import textwrap

LINE_WIDTH = 70
TIMESTAMP_PREFIX_LEN = 11  # len("[HH:MM:SS] ")
SEPARATOR = "=" * 40


def format_transcript(metadata: dict, segments: list) -> str:
    lines = [
        SEPARATOR,
        " TRANSCRIPTION",
        SEPARATOR,
        f" File     : {metadata['filename']}",
        f" Date     : {metadata['date']}",
        f" Duration : {_format_duration(metadata['duration'])}",
        f" Language : {metadata['language']}",
        f" Model    : whisper-{metadata['model']}",
        SEPARATOR,
        "",
    ]

    for segment in segments:
        text = segment["text"].strip()
        if not text:
            continue

        prefix = f"{_format_timestamp(segment['start'])} "
        indent = " " * TIMESTAMP_PREFIX_LEN

        wrapped = textwrap.fill(
            text,
            width=LINE_WIDTH,
            initial_indent=prefix,
            subsequent_indent=indent,
        )
        lines.append(wrapped)
        lines.append("")

    lines += [SEPARATOR, " END OF TRANSCRIPTION", SEPARATOR]
    return "\n".join(lines)


def _format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"[{h:02d}:{m:02d}:{s:02d}]"


def _format_duration(seconds: float) -> str:
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
