# 
#   NatML
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from __future__ import annotations
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from .api import query
from .audio import AudioFormat
from .license import License
from .normalization import Normalization
from .profile import Profile
from .upload import Storage, UploadType

class AccessMode (str, Enum):
    """
    Predictor access mode.
    """
    Public = "PUBLIC"
    Private = "PRIVATE"

class AspectMode (str, Enum):
    """
    Image aspect mode.
    """
    ScaleToFit = "SCALE_TO_FIT"
    AspectFill = "ASPECT_FILL"
    AspectFit = "ASPECT_FIT"

class PredictorStatus (str, Enum):
    """
    Predictor status.
    """
    Draft = "DRAFT"
    Published = "PUBLISHED"
    Archived = "ARCHIVED"

@dataclass
class Predictor:
    """
    Predictor.

    Members:
        tag (str): Predictor tag.
        owner (Profile): Predictor owner.
        name (str): Predictor name.
        description (str): Predictor description.
        status (PredictorStatus): Predictor status.
        access (AccessMode): Predictor access.
        graphs (list): Predictor graphs.
        endpoints (list): Predictor endpoints.
        license (License): Predictor license.
        topics (list): Predictor topics.
        created (str): Date created.
        media (str): Predictor media.
        labels (list): Classification labels.
        normalization (Normalization): Feature normalization.
        aspectMode (AspectMode): Image aspect mode.
        audioFormat (AudioFormat): Audio format.
    """
    tag: str
    owner: Profile
    name: str
    description: str
    status: PredictorStatus
    access: AccessMode
    license: License
    topics: Optional[List[str]] = None
    created: Optional[str] = None
    media: Optional[str] = None
    labels: Optional[List[str]] = None
    normalization: Optional[Normalization] = None
    aspect_mode: Optional[AspectMode] = None
    audio_format: Optional[AudioFormat] = None

    def __post_init__ (self):
        self.owner = Profile(**self.owner, email=None) if isinstance(self.owner, dict) else self.owner
        self.normalization = Normalization(**self.normalization) if isinstance(self.normalization, dict) else self.normalization
        self.audio_format = AudioFormat(**self.audio_format) if isinstance(self.audio_format, dict) else self.audio_format

    @classmethod
    def retrieve (
        cls,
        tag: str,
        access_key: str=None
    ) -> Predictor:
        """
        Retrieve a predictor.

        Parameters:
            tag (str): Predictor tag. This MUST NOT be a variant tag.
            access_key (str): NatML access key.

        Returns:
            Predictor: Predictor.
        """
        # Query
        response = query(f"""
            query ($input: PredictorInput!) {{
                predictor (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                }}
            }}
            """,
            { "tag": tag },
            access_key=access_key
        )
        # Create predictor
        predictor = response["predictor"]
        predictor = Predictor(**predictor) if predictor else None
        # Return
        return predictor

    @classmethod
    def list (
        cls,
        mine: bool=False,
        status: PredictorStatus=None,
        offset: int=None,
        count: int=None,
        access_key: str=None
    ) -> List[Predictor]:
        """
        View available predictors.
        
        Parameters:
            mine (bool): Fetch only predictors owned by me.
            status (PredictorStatus): Predictor status. This only applies when `mine` is `True`.
            offset (int): Pagination offset.
            count (int): Pagination count.
            access_key (str): NatML access key.

        Returns:
            list: Predictors.
        """
        # Collect inputs
        input = { "mine": mine, "status": status, "offset": offset, "count": count }
        input = { k: v for k, v in input.items() if v is not None }
        # Query
        response = query(f"""
            query ($input: PredictorsInput!) {{
                predictors (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                }}
            }}
            """,
            input,
            access_key=access_key
        )
        # Create predictors
        predictors = response["predictors"]
        predictors = [Predictor(**predictor) for predictor in predictors]
        # Return
        return predictors

    @classmethod
    def search (
        cls,
        query: str,
        offset: int=None,
        count: int=None,
        access_key: str=None
    ) -> List[Predictor]:
        """
        Search predictors.

        Parameters:
            query (str): Search query.
            access_key (str): NatML access key.

        Returns:
            list: Relevant predictors.
        """
        # Query
        response = query(f"""
            query ($input: PredictorsInput!) {{
                predictors (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                }}
            }}
            """,
            { "query": query, "offset": offset, "count": count },
            access_key=access_key
        )
        # Create predictors
        predictors = response["predictors"]
        predictors = [Predictor(**predictor) for predictor in predictors]
        # Return
        return predictors

    @classmethod
    def create (
        cls,
        tag: str,
        description: str=None,
        access: AccessMode=AccessMode.Private,
        access_key: str=None
    ) -> Predictor:
        """
        Create a predictor.

        Parameters:
            tag (str): Predictor tag.
            description (str): Predictor description. This supports Markdown.
            access (AccessMode): Predictor access mode.
            access_key (str): NatML access key.

        Returns:
            Predictor: Created predictor.
        """
        # Query
        response = query(f"""
            mutation ($input: CreatePredictorInput!) {{
                createPredictor (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                    normalization {{
                        mean
                        std
                    }}
                    aspect_mode: aspectMode
                    audio_format: audioFormat {{
                        sample_rate: sampleRate
                        channel_count: channelCount
                    }}
                }}
            }}
            """,
            { "tag": tag, "description": description, "access": access },
            access_key=access_key
        )
        # Create predictor
        predictor = response["createPredictor"]
        predictor = Predictor(**predictor) if predictor else None
        # Return
        return predictor

    @classmethod
    def update (
        cls,
        tag: str,
        description: str=None,
        access: AccessMode=None,
        license: License=None,
        topics: List[str]=None,
        media: Union[str,Path]=None,
        labels: List[str]=None,
        normalization: Normalization=None,
        aspect_mode: AspectMode=None,
        audio_format: AudioFormat=None,
        delete_media: bool=False,
        delete_labels: bool=False,
        delete_normalization: bool=False,
        delete_aspect_mode: bool=False,
        delete_audio_format: bool=False,
        access_key: str=None
    ) -> Predictor:
        """
        Update a predictor.

        Parameters:
            tag (str): Predictor tag.
            description (str): Predictor description. This supports Markdown.
            access (AccessMode): Predictor access mode.
            license (License): Predictor license.
            topics (list): Predictor topics.
            media (str | Path): Predictor media URL or path. Pass an empty string to unset.
            labels (list): Classification labels.
            normalization (Normalization): Feature normalization.
            aspect_mode (AspectMode): Image aspect mode.
            audio_format (AudioFormat): Audio format.
            delete_media (bool): Delete existing media.
            delete_labels (bool): Delete existing classification labels.
            delete_normalization (bool): Delete existing feature normalization.
            delete_aspect_mode (bool): Delete existing image aspect mode.
            delete_audio_format (bool): Delete existing audio format.
            access_key (str): NatML access key.

        Returns:
            Predictor: Updated predictor.
        """
        # Upload media
        media = Storage.upload(media, UploadType.Media, check_extension=True) if isinstance(media, Path) else media
        # Gather inputs
        preserve_keys = [k for k, v in {
            "media": delete_media,
            "labels": delete_labels,
            "normalization": delete_normalization,
            "aspectMode": delete_aspect_mode,
            "audioFormat": delete_audio_format
        }.items() if v]
        input = {
            "tag": tag,
            "description": description,
            "access": access,
            "license": license,
            "topics": topics,
            "media": media,
            "labels": labels,
            "normalization": asdict(normalization) if normalization else None,
            "aspectMode": aspect_mode,
            "audioFormat": { "sampleRate": audio_format.sample_rate, "channelCount": audio_format.channel_count } if audio_format else None,
        }
        input = { k: v for k, v in input.items() if v is not None or k in preserve_keys }
        # Query
        response = query(f"""
            mutation ($input: UpdatePredictorInput!) {{
                updatePredictor (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                    normalization {{
                        mean
                        std
                    }}
                    aspect_mode: aspectMode
                    audio_format: audioFormat {{
                        sample_rate: sampleRate
                        channel_count: channelCount
                    }}
                }}
            }}
            """,
            input,
            access_key=access_key
        )
        # Create predictor
        predictor = response["updatePredictor"]
        predictor = Predictor(**predictor) if predictor else None
        # Return
        return predictor

    @classmethod
    def delete (
        cls,
        tag: str,
        access_key: str=None
    ) -> bool:
        """
        Delete a draft predictor.

        Parameters:
            tag (str): Predictor tag.
            access_key (str): NatML access key.

        Returns:
            bool: Whether the predictor was successfully deleted.
        """
        # Query
        response = query(f"""
            mutation ($input: DeletePredictorInput!) {{
                deletePredictor (input: $input)
            }}
            """,
            { "tag": tag },
            access_key=access_key
        )
        # Return
        result = response["deletePredictor"]
        return result

    @classmethod
    def review (
        cls,
        tag: str,
        access_key: str=None  
    ) -> List[str]:
        """
        Review a draft predictor for any issues that might prevent it from being published.

        Parameters:
            tag (str): Predictor tag.
            access_key (str): NatML access key.

        Returns:
            list: Issues that might prevent the predictor from being published. Empty array means no issues were found.
        """
        # Query
        response = query(f"""
            mutation ($input: ReviewPredictorInput!) {{
                reviewPredictor (input: $input)
            }}
            """,
            { "tag": tag },
            access_key=access_key
        )
        # Return
        result = response["reviewPredictor"]
        return result

    @classmethod
    def publish (
        cls,
        tag: str,
        access_key: str=None
    ) -> Predictor:
        """
        Publish a draft predictor.

        Parameters:
            tag (str): Predictor tag.
            access_key (str): NatML access key.

        Returns:
            Predictor: Published predictor.
        """
        # Query
        response = query(f"""
            mutation ($input: PublishPredictorInput!) {{
                publishPredictor (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                }}
            }}
            """,
            { "tag": tag },
            access_key=access_key
        )
        # Create predictor
        predictor = response["publishPredictor"]
        predictor = Predictor(**predictor) if predictor else None
        # Return
        return predictor

    @classmethod
    def archive (
        cls,
        tag: str,
        access_key: str=None
    ) -> Predictor:
        """
        Archive a published predictor.

        Parameters:
            tag (str): Predictor tag.
            access_key (str): NatML access key.

        Returns:
            Predictor: Archived predictor.
        """
        # Query
        response = query(f"""
            mutation ($input: ArchivePredictorInput!) {{
                archivePredictor (input: $input) {{
                    tag
                    owner {{
                        username
                        created
                        name
                        avatar
                        bio
                        website
                        github
                    }}
                    name
                    description
                    status
                    access
                    license
                    topics
                    created
                    media
                }}
            }}
            """,
            { "tag": tag },
            access_key=access_key
        )
        # Create predictor
        predictor = response["archivePredictor"]
        predictor = Predictor(**predictor) if predictor else None
        # Return
        return predictor