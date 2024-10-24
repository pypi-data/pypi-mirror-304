"""
Nice help: https://www.bannerbear.com/blog/how-to-use-ffmpeg-in-python-with-examples/
Official doc: https://www.ffmpeg.org/ffmpeg-resampler.html
More help: https://kkroening.github.io/ffmpeg-python/

Interesting usage: https://stackoverflow.com/a/20325676
Maybe avoid writting on disk?: https://github.com/kkroening/ffmpeg-python/issues/500#issuecomment-792281072
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.audio.parser import AudioParser
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.writer import write_file

import ffmpeg


class FfmpegAudioCodec(Enum):
    AAC = 'aac'
    """
    Default encoder.
    """
    AC3 = 'ac3'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    AC3_FIXED = 'ac3_fixed'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    FLAC = 'flac'
    """
    FLAC (Free Lossless Audio Codec) Encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-flac-2
    """
    OPUS = 'opus'
    """
    This is a native FFmpeg encoder for the Opus format. Currently, it’s
    in development and only implements the CELT part of the codec. Its
    quality is usually worse and at best is equal to the libopus encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-opus
    """
    LIBFDK_AAC = 'libfdk_aac'
    """
    libfdk-aac AAC (Advanced Audio Coding) encoder wrapper. The libfdk-aac
    library is based on the Fraunhofer FDK AAC code from the Android project.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libfdk_005faac
    """
    LIBLC3 = 'liblc3'
    """
    liblc3 LC3 (Low Complexity Communication Codec) encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-liblc3
    """
    LIBMP3LAME = 'libmp3lame'
    """
    LAME (Lame Ain’t an MP3 Encoder) MP3 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libmp3lame-1
    """
    LIBOPENCORE_AMRNB = 'libopencore_amrnb'
    """
    OpenCORE Adaptive Multi-Rate Narrowband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopencore_002damrnb-1ss
    """
    LIBOPUS = 'libopus'
    """
    libopus Opus Interactive Audio Codec encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopus-1
    """
    LIBSHINE = 'libshine'
    """
    Shine Fixed-Point MP3 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libshine-1
    """
    LIBTWOLAME = 'libtwolame'
    """
    TwoLAME MP2 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libtwolame
    """
    LIBVO_AMRWBENC = 'libvo-amrwbenc'
    """
    VisualOn Adaptive Multi-Rate Wideband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvo_002damrwbenc
    """
    LIBVORBIS = 'libvorbis'
    """
    libvorbis encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvorbis
    """
    MJPEG = 'mjpeg'
    """
    Motion JPEG encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-mjpeg
    """
    WAVPACK = 'wavpack'
    """
    WavPack lossless audio encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-wavpack
    """

class FfmpegVideoCodec(Enum):
    A64_MULTI = 'a64_multi'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    A64_MULTI5 = 'a64_multi5'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    CINEPAK = 'Cinepak'
    """
    Cinepak aka CVID encoder. Compatible with Windows 3.1 and vintage MacOS.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    GIF = 'GIF'
    """
    GIF image/animation encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    HAP = 'Hap'
    """
    Vidvox Hap video encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Hap
    """
    JPEG2000 = 'jpeg2000'
    """
    The native jpeg 2000 encoder is lossy by default

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-jpeg2000
    """
    LIBRAV1E = 'librav1e'
    """
    rav1e AV1 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-librav1e
    """
    LIBAOM_AV1 = 'libaom-av1'
    """
    libaom AV1 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libaom_002dav1
    """
    # TODO: Continue with this (https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libsvtav1)


class FfmpegHandler:
    """
    Class to simplify and encapsulate ffmpeg functionality.
    """
    @classmethod
    def _validate_video_filename(cls, video_filename: str):
        # TODO: Validate and raise Exception if invalid
        pass

    @classmethod
    def _write_concat_file(cls, filenames: str):
        """
        Writes the files to concat in a temporary text file with
        the required format and returns that file filename.
        """
        text = ''
        for filename in filenames:
            text += f"file '{filename}'\n"

        # TODO: Maybe this below is interesting for the file.writer
        # open('concat.txt', 'w').writelines([('file %s\n' % input_path) for input_path in input_paths])
        filename = create_temp_filename('concat_ffmpeg.txt')
        write_file(text, filename)

        return filename

    @classmethod
    def get_audio_from_video(cls, video_filename: str, codec: FfmpegAudioCodec = None, output_filename: str = None):
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.
        """
        cls._validate_video_filename(video_filename)
        
        if not output_filename:
            output_filename = create_temp_filename('temp_audio.mp3')
        # TODO: Verify valid extension

        if codec:
            codec = FfmpegAudioCodec.to_enum(codec)

        ffmpeg.input(video_filename).output(output_filename, acodec = codec).run()

        return AudioParser.to_audiofileclip(output_filename)

    @classmethod
    def get_best_thumbnail(cls, video_filename: str, output_filename: str = None):
        """
        Gets the best thumbnail of the provided 'video_filename'.
        """
        cls._validate_video_filename(video_filename)

        if not output_filename:
            output_filename = create_temp_filename('temp_thumbnail.png')
        # TODO: Verify valid extension

        ffmpeg.input(video_filename).filter('thumbnail').output(output_filename).run()

        return ImageParser.to_pillow(output_filename)
    
    @classmethod
    def concatenate_videos(cls, video_filenames: str, output_filename: str = None):
        """
        Concatenates the provided 'video_filenames' in the order in
        which they are provided.
        """
        for video_filename in video_filenames:
            cls._validate_video_filename(video_filename)

        if not output_filename:
            output_filename = create_temp_filename('concatenated_video.mp4')

        concat_filename = cls._write_concat_file(video_filenames)

        # This is the original to concat with ffmpeg 
        # command = 'ffmpeg -y -f concat -safe 0 -i ' + filename + ' -c copy ' + output_abspath
        ffmpeg.input(concat_filename, format = 'concat', safe = 0).output(output_filename, c = 'copy').run(overwrite_output = True)

        #ffmpeg.concat(input_video, v = 1).output(output_filename).run(overwrite_output = True)

        return VideoParser.to_moviepy(output_filename)
    
    # TODO: Keep going