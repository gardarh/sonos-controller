from typing import Any

import soco  # type: ignore[import-untyped]
from soco import SoCo  # type: ignore[import-untyped]


def discover_speakers() -> list[dict[str, str]]:
    speakers = soco.discover()
    if not speakers:
        return []
    return [
        {"name": speaker.player_name, "ip": speaker.ip_address} for speaker in speakers
    ]


def get_speaker_by_name(name: str) -> SoCo | None:
    speakers = soco.discover()
    if not speakers:
        return None
    for speaker in speakers:
        if speaker.player_name == name:
            return speaker
    return None


def get_speaker_info(speaker_name: str) -> dict[str, Any] | None:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return None
    track = speaker.get_current_track_info()

    # media_info = speaker.get_current_media_info()
    transport_info = speaker.get_current_transport_info()
    return {
        "name": speaker.player_name,
        "ip": speaker.ip_address,
        "volume": speaker.volume,
        "mute": speaker.mute,
        "playback_state": transport_info.get("current_transport_state"),
        "music_source": speaker.music_source,
        "current_track": {
            "title": track.get("title"),
            "artist": track.get("artist"),
            "album": track.get("album"),
            "uri": track.get("uri"),
        },
    }


def play(speaker_name: str) -> bool:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return False
    speaker.play()
    return True


def pause(speaker_name: str) -> bool:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return False
    speaker.pause()
    return True


def set_source(speaker_name: str, source: str) -> tuple[bool, str | None]:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return False, "Speaker not found"
    if source == "line-in":
        speaker.switch_to_line_in()
    elif source == "music":
        speaker.play_from_queue(0)
    else:
        return False, f"Unknown source: {source}. Valid sources: line-in, music"
    return True, None


def set_volume(speaker_name: str, volume: int) -> bool:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return False
    speaker.volume = volume
    return True


def play_uri(speaker_name: str, uri: str, title: str = "") -> bool:
    speaker = get_speaker_by_name(speaker_name)
    if not speaker:
        return False
    speaker.play_uri(uri, title=title)
    return True
