"""gr.WebRTC() component."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
import logging
import threading
import time
import traceback
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Generator, Literal, Sequence, cast

import anyio.to_thread
import numpy as np
from aiortc import (
    AudioStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
    MediaStreamTrack,
)
import av
from aiortc.contrib.media import MediaRelay, AudioFrame, VideoFrame  # type: ignore
from aiortc.mediastreams import MediaStreamError
from gradio import wasm_utils
from gradio.components.base import Component, server
from gradio_client import handle_file

from gradio_webrtc.utils import player_worker_decode, player_worker_decode_generator

if TYPE_CHECKING:
    from gradio.blocks import Block
    from gradio.components import Timer
    from gradio.events import Dependency


if wasm_utils.IS_WASM:
    raise ValueError("Not supported in gradio-lite!")


logger = logging.getLogger(__name__)


class VideoCallback(VideoStreamTrack):
    """
    This works for streaming input and output
    """

    kind = "video"

    def __init__(
        self,
        track: MediaStreamTrack,
        event_handler: Callable,
    ) -> None:
        super().__init__()  # don't forget this!
        self.track = track
        self.event_handler = event_handler
        self.latest_args: str | list[Any] = "not_set"

    def add_frame_to_payload(
        self, args: list[Any], frame: np.ndarray | None
    ) -> list[Any]:
        new_args = []
        for val in args:
            if isinstance(val, str) and val == "__webrtc_value__":
                new_args.append(frame)
            else:
                new_args.append(val)
        return new_args

    def array_to_frame(self, array: np.ndarray) -> VideoFrame:
        return VideoFrame.from_ndarray(array, format="bgr24")

    async def recv(self):
        try:
            try:
                frame = cast(VideoFrame, await self.track.recv())
            except MediaStreamError:
                return
            frame_array = frame.to_ndarray(format="bgr24")

            if self.latest_args == "not_set":
                return frame

            args = self.add_frame_to_payload(cast(list, self.latest_args), frame_array)

            array = self.event_handler(*args)

            new_frame = self.array_to_frame(array)
            if frame:
                new_frame.pts = frame.pts
                new_frame.time_base = frame.time_base
            else:
                pts, time_base = await self.next_timestamp()
                new_frame.pts = pts
                new_frame.time_base = time_base

            return new_frame
        except Exception as e:
            logger.debug(e)
            exec = traceback.format_exc()
            logger.debug(exec)


class StreamHandler(ABC):

    def __init__(self,
                 expected_layout: Literal["mono", "stereo"] = "mono",
                 output_sample_rate: int = 24000,
                 output_frame_size: int = 960) -> None:
        self.expected_layout = expected_layout
        self.output_sample_rate = output_sample_rate
        self.output_frame_size = output_frame_size
        self._resampler = None
    
    def resample(self, frame: AudioFrame) -> Generator[AudioFrame, None, None]:
        if self._resampler is None:
            self._resampler = av.AudioResampler(
                format="s16",
                layout=self.expected_layout,
                rate=frame.sample_rate,
                frame_size=frame.samples,
            )
        yield from self._resampler.resample(frame)

    @abstractmethod
    def receive(self, frame: tuple[int, np.ndarray] | np.ndarray) -> None:
        pass

    @abstractmethod
    def emit(self) -> None:
        pass


class AudioCallback(AudioStreamTrack):
    kind = "audio"

    def __init__(
        self,
        track: MediaStreamTrack,
        event_handler: StreamHandler,
    ) -> None:
        self.track = track
        self.event_handler = event_handler
        self.current_timestamp = 0
        self.latest_args = "not_set"
        self.queue = asyncio.Queue()
        self.thread_quit = threading.Event()
        self.__thread = None
        self._start: float | None = None
        self.has_started = False
        super().__init__()

    async def process_input_frames(self) -> None:
        while not self.thread_quit.is_set():
            try:
                frame = cast(AudioFrame, await self.track.recv())
                for frame in self.event_handler.resample(frame):
                    numpy_array = frame.to_ndarray()
                    logger.debug("numpy array shape %s", numpy_array.shape)
                    await anyio.to_thread.run_sync(
                        self.event_handler.receive, (frame.sample_rate, numpy_array)
                    )
            except MediaStreamError as e:
                print("MediaStreamError", e)
                break

    def start(self):
        if not self.has_started:
            asyncio.create_task(self.process_input_frames())
            self.__thread = threading.Thread(
                name="audio-output-decoders",
                target=player_worker_decode,
                args=(
                    asyncio.get_event_loop(),
                    self.event_handler.emit,
                    self.queue,
                    False,
                    self.thread_quit,
                    False,
                    self.event_handler.output_sample_rate,
                    self.event_handler.output_frame_size,
                ),
            )
            self.__thread.start()
            self.has_started = True

    async def recv(self):
        try:
            if self.readyState != "live":
                raise MediaStreamError

            self.start()
            frame = await self.queue.get()
            logger.debug("frame %s", frame)

            data_time = frame.time
            print("data_time", data_time)

            # control playback rate
            # if self._time_last_msg:
            #     wait = self._time_last_msg + self.freq - time.time()
            #     print("wait", wait)
            #     await asyncio.sleep(wait)
            self._time_last_msg = time.time()

            return frame
        except Exception as e:
            logger.debug(e)
            exec = traceback.format_exc()
            logger.debug(exec)

    def stop(self):
        self.thread_quit.set()
        if self.__thread is not None:
            self.__thread.join()
            self.__thread = None
        super().stop()


class ServerToClientVideo(VideoStreamTrack):
    """
    This works for streaming input and output
    """

    kind = "video"

    def __init__(
        self,
        event_handler: Callable,
    ) -> None:
        super().__init__()  # don't forget this!
        self.event_handler = event_handler
        self.latest_args: str | list[Any] = "not_set"
        self.generator: Generator[Any, None, Any] | None = None

    def array_to_frame(self, array: np.ndarray) -> VideoFrame:
        return VideoFrame.from_ndarray(array, format="bgr24")

    async def recv(self):
        try:
            pts, time_base = await self.next_timestamp()
            if self.latest_args == "not_set":
                frame = self.array_to_frame(np.zeros((480, 640, 3), dtype=np.uint8))
                frame.pts = pts
                frame.time_base = time_base
                return frame
            elif self.generator is None:
                self.generator = cast(
                    Generator[Any, None, Any], self.event_handler(*self.latest_args)
                )

            try:
                next_array = next(self.generator)
            except StopIteration:
                self.stop()
                return

            next_frame = self.array_to_frame(next_array)
            next_frame.pts = pts
            next_frame.time_base = time_base
            return next_frame
        except Exception as e:
            logger.debug(e)
            exec = traceback.format_exc()
            logger.debug(exec)


class ServerToClientAudio(AudioStreamTrack):
    kind = "audio"

    def __init__(
        self,
        event_handler: Callable,
    ) -> None:
        self.generator: Generator[Any, None, Any] | None = None
        self.event_handler = event_handler
        self.current_timestamp = 0
        self.latest_args = "not_set"
        self.queue = asyncio.Queue()
        self.thread_quit = threading.Event()
        self.__thread = None
        self._start: float | None = None
        super().__init__()

    def next(self) -> tuple[int, np.ndarray] | None:
        if self.latest_args == "not_set":
            return
        if self.generator is None:
            self.generator = self.event_handler(*self.latest_args)
        if self.generator is not None:
            try:
                frame = next(self.generator)
                return frame
            except Exception as exc:
                if isinstance(exc, StopIteration):
                    logger.debug("Stopping audio stream")
                    asyncio.run_coroutine_threadsafe(
                        self.queue.put(None), asyncio.get_event_loop()
                    )
                    self.thread_quit.set()

    def start(self):
        if self.__thread is None:
            self.__thread = threading.Thread(
                name="generator-runner",
                target=player_worker_decode,
                args=(
                    asyncio.get_event_loop(),
                    self.next,
                    self.queue,
                    False,
                    self.thread_quit,
                    True,
                ),
            )
            self.__thread.start()

    async def recv(self):
        try:
            if self.readyState != "live":
                raise MediaStreamError

            self.start()
            data = await self.queue.get()
            if data is None:
                self.stop()
                return

            data_time = data.time

            # control playback rate
            if data_time is not None:
                if self._start is None:
                    self._start = time.time() - data_time
                else:
                    wait = self._start + data_time - time.time()
                    await asyncio.sleep(wait)

            return data
        except Exception as e:
            logger.debug(e)
            exec = traceback.format_exc()
            logger.debug(exec)

    def stop(self):
        self.thread_quit.set()
        if self.__thread is not None:
            self.__thread.join()
            self.__thread = None
        super().stop()

from gradio.events import Dependency

class WebRTC(Component):
    """
    Creates a video component that can be used to upload/record videos (as an input) or display videos (as an output).
    For the video to be playable in the browser it must have a compatible container and codec combination. Allowed
    combinations are .mp4 with h264 codec, .ogg with theora codec, and .webm with vp9 codec. If the component detects
    that the output video would not be playable in the browser it will attempt to convert it to a playable mp4 video.
    If the conversion fails, the original video is returned.

    Demos: video_identity_2
    """

    pcs: set[RTCPeerConnection] = set([])
    relay = MediaRelay()
    connections: dict[
        str, VideoCallback | ServerToClientVideo | ServerToClientAudio | AudioCallback
    ] = {}

    EVENTS = ["tick"]

    def __init__(
        self,
        value: None = None,
        height: int | str | None = None,
        width: int | str | None = None,
        label: str | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        mirror_webcam: bool = True,
        rtc_configuration: dict[str, Any] | None = None,
        track_constraints: dict[str, Any] | None = None,
        time_limit: float | None = None,
        mode: Literal["send-receive", "receive"] = "send-receive",
        modality: Literal["video", "audio"] = "video",
    ):
        """
        Parameters:
            value: path or URL for the default value that WebRTC component is going to take. Can also be a tuple consisting of (video filepath, subtitle filepath). If a subtitle file is provided, it should be of type .srt or .vtt. Or can be callable, in which case the function will be called whenever the app loads to set the initial value of the component.
            format: the file extension with which to save video, such as 'avi' or 'mp4'. This parameter applies both when this component is used as an input to determine which file format to convert user-provided video to, and when this component is used as an output to determine the format of video returned to the user. If None, no file format conversion is done and the video is kept as is. Use 'mp4' to ensure browser playability.
            height: The height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. This has no effect on the preprocessed video file, but will affect the displayed video.
            width: The width of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. This has no effect on the preprocessed video file, but will affect the displayed video.
            label: the label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            show_label: if True, will display label.
            container: if True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will allow users to upload a video; if False, can only be used to display videos. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: if False, component will be hidden.
            elem_id: an optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: an optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: if False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            mirror_webcam: if True webcam will be mirrored. Default is True.
            include_audio: whether the component should record/retain the audio track for a video. By default, audio is excluded for webcam videos and included for uploaded videos.
            autoplay: whether to automatically play the video when the component is used as an output. Note: browsers will not autoplay video files if the user has not interacted with the page yet.
            show_share_button: if True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.
            show_download_button: if True, will show a download icon in the corner of the component that allows user to download the output. If False, icon does not appear. By default, it will be True for output components and False for input components.
            min_length: the minimum length of video (in seconds) that the user can pass into the prediction function. If None, there is no minimum length.
            max_length: the maximum length of video (in seconds) that the user can pass into the prediction function. If None, there is no maximum length.
            loop: if True, the video will loop when it reaches the end and continue playing from the beginning.
            streaming: when used set as an output, takes video chunks yielded from the backend and combines them into one streaming video output. Each chunk should be a video file with a .ts extension using an h.264 encoding. Mp4 files are also accepted but they will be converted to h.264 encoding.
            watermark: an image file to be included as a watermark on the video. The image is not scaled and is displayed on the bottom right of the video. Valid formats for the image are: jpeg, png.
        """
        self.time_limit = time_limit
        self.height = height
        self.width = width
        self.mirror_webcam = mirror_webcam
        self.concurrency_limit = 1
        self.rtc_configuration = rtc_configuration
        self.mode = mode
        self.modality = modality
        if track_constraints is None and modality == "audio":
            track_constraints = {
                "echoCancellation": True,
                "noiseSuppression": {"exact": True},
                "autoGainControl": {"exact": True},
                "sampleRate": {"ideal": 24000},
                "sampleSize": {"ideal": 16},
                "channelCount": {"exact": 1},
            }
        if track_constraints is None and modality == "video":
            track_constraints = {
                "facingMode": "user",
                "width": {"ideal": 500},
                "height": {"ideal": 500},
                "frameRate": {"ideal": 30},
            }
        self.track_constraints = track_constraints
        self.event_handler: Callable | StreamHandler | None = None
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            value=value,
        )

    def preprocess(self, payload: str) -> str:
        """
        Parameters:
            payload: An instance of VideoData containing the video and subtitle files.
        Returns:
            Passes the uploaded video as a `str` filepath or URL whose extension can be modified by `format`.
        """
        return payload

    def postprocess(self, value: Any) -> str:
        """
        Parameters:
            value: Expects a {str} or {pathlib.Path} filepath to a video which is displayed, or a {Tuple[str | pathlib.Path, str | pathlib.Path | None]} where the first element is a filepath to a video and the second element is an optional filepath to a subtitle file.
        Returns:
            VideoData object containing the video and subtitle files.
        """
        return value

    def set_output(self, webrtc_id: str, *args):
        if webrtc_id in self.connections:
            if self.mode == "send-receive":
                self.connections[webrtc_id].latest_args = ["__webrtc_value__"] + list(
                    args
                )
            elif self.mode == "receive":
                self.connections[webrtc_id].latest_args = list(args)
                self.connections[webrtc_id].args_set.set()  # type: ignore

    def stream(
        self,
        fn: Callable[..., Any] | StreamHandler | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | set[Block] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        time_limit: float | None = None,
        trigger: Dependency | None = None,
    ):
        from gradio.blocks import Block

        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        if isinstance(inputs, Block):
            inputs = [inputs]
        if isinstance(outputs, Block):
            outputs = [outputs]

        self.concurrency_limit = (
            1 if concurrency_limit in ["default", None] else concurrency_limit
        )
        self.event_handler = fn
        self.time_limit = time_limit

        if (
            self.mode == "send-receive"
            and self.modality == "audio"
            and not isinstance(self.event_handler, StreamHandler)
        ):
            raise ValueError(
                "In the send-receive mode for audio, the event handler must be an instance of StreamHandler."
            )

        if self.mode == "send-receive":
            if cast(list[Block], inputs)[0] != self:
                raise ValueError(
                    "In the webrtc stream event, the first input component must be the WebRTC component."
                )

            if (
                len(cast(list[Block], outputs)) != 1
                and cast(list[Block], outputs)[0] != self
            ):
                raise ValueError(
                    "In the webrtc stream event, the only output component must be the WebRTC component."
                )
            return self.tick(  # type: ignore
                self.set_output,
                inputs=inputs,
                outputs=None,
                concurrency_id=concurrency_id,
                concurrency_limit=None,
                stream_every=0.5,
                time_limit=None,
                js=js,
            )
        elif self.mode == "receive":
            if isinstance(inputs, list) and self in cast(list[Block], inputs):
                raise ValueError(
                    "In the receive mode stream event, the WebRTC component cannot be an input."
                )
            if (
                len(cast(list[Block], outputs)) != 1
                and cast(list[Block], outputs)[0] != self
            ):
                raise ValueError(
                    "In the receive mode stream, the only output component must be the WebRTC component."
                )
            if trigger is None:
                raise ValueError(
                    "In the receive mode stream event, the trigger parameter must be provided"
                )
            trigger(lambda: "start_webrtc_stream", inputs=None, outputs=self)
            self.tick(  # type: ignore
                self.set_output,
                inputs=[self] + list(inputs),
                outputs=None,
                concurrency_id=concurrency_id,
            )

    @staticmethod
    async def wait_for_time_limit(pc: RTCPeerConnection, time_limit: float):
        await asyncio.sleep(time_limit)
        await pc.close()

    @server
    async def offer(self, body):
        logger.debug("Starting to handle offer")
        logger.debug("Offer body %s", body)
        if len(self.connections) >= cast(int, self.concurrency_limit):
            return {"status": "failed"}

        offer = RTCSessionDescription(sdp=body["sdp"], type=body["type"])

        pc = RTCPeerConnection()
        self.pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            logger.debug("ICE connection state change %s", pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.connections.pop(body["webrtc_id"], None)
                self.pcs.discard(pc)

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.debug("pc.connectionState %s", pc.connectionState)
            if pc.connectionState in ["failed", "closed"]:
                await pc.close()
                connection = self.connections.pop(body["webrtc_id"], None)
                if connection:
                    connection.stop()
                self.pcs.discard(pc)
            if pc.connectionState == "connected":
                if self.time_limit is not None:
                    asyncio.create_task(self.wait_for_time_limit(pc, self.time_limit))

        @pc.on("track")
        def on_track(track):
            relay = MediaRelay()
            if self.modality == "video":
                cb = VideoCallback(
                    relay.subscribe(track),
                    event_handler=cast(Callable, self.event_handler),
                )
            elif self.modality == "audio":
                cb = AudioCallback(
                    relay.subscribe(track),
                    event_handler=cast(StreamHandler, self.event_handler),
                )
            self.connections[body["webrtc_id"]] = cb
            logger.debug("Adding track to peer connection %s", cb)
            pc.addTrack(cb)

        if self.mode == "receive":
            if self.modality == "video":
                cb = ServerToClientVideo(cast(Callable, self.event_handler))
            elif self.modality == "audio":
                cb = ServerToClientAudio(cast(Callable, self.event_handler))

            logger.debug("Adding track to peer connection %s", cb)
            pc.addTrack(cb)
            self.connections[body["webrtc_id"]] = cb
            cb.on("ended", lambda: self.connections.pop(body["webrtc_id"], None))

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)  # type: ignore
        logger.debug("done handling offer about to return")

        return {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type,
        }

    def example_payload(self) -> Any:
        return {
            "video": handle_file(
                "https://github.com/gradio-app/gradio/raw/main/demo/video_component/files/world.mp4"
            ),
        }

    def example_value(self) -> Any:
        return "https://github.com/gradio-app/gradio/raw/main/demo/video_component/files/world.mp4"

    def api_info(self) -> Any:
        return {"type": "number"}
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer

    
    def tick(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        
        """
        ...