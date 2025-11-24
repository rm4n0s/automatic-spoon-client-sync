from pydantic import BaseModel, Field

from .enums import (
    AIModelBase,
    AIModelType,
    ControlNetType,
    FileImageType,
    LongPromptTechnique,
    PathType,
    Scheduler,
    Variant,
)


class ControlNetImageInput(BaseModel):
    aimodel_id: (
        int | None
    )  # if none is image reference to be used from engine's controlnets
    data_base64: str
    controlnet_conditioning_scale: float


class ImageUserInput(BaseModel):
    prompt: str
    negative_prompt: str
    seed: int | None = Field(default=None)
    guidance_scale: float | None = Field(default=None)
    width: int | None = Field(default=None)
    height: int | None = Field(default=None)
    steps: int | None = Field(default=None)
    control_images: list[ControlNetImageInput] = Field(default=[])
    file_type: FileImageType = Field(default=FileImageType.PNG)
    control_guidance_start: float | None = None
    control_guidance_end: float | None = None


class JobUserInput(BaseModel):
    generator_id: int
    images: list[ImageUserInput]


class GeneratorUserInput(BaseModel):
    name: str
    engine_id: int
    gpu_id: int = Field(default=0)


class LoraIDAndWeight(BaseModel):
    lora_id: int
    weight: int


class EngineUserInput(BaseModel):
    name: str
    checkpoint_model_id: int
    scheduler: Scheduler
    guidance_scale: float
    seed: int
    width: int
    height: int
    steps: int
    lora_model_ids: list[LoraIDAndWeight] = Field(default=[])
    conrol_net_model_ids: list[int] = Field(default=[])
    embedding_model_ids: list[int] = Field(default=[])
    long_prompt_technique: LongPromptTechnique | None = None
    vae_model_id: int | None = None
    controlnet_conditioning_scale: float | None = None
    control_guidance_start: float | None = None
    control_guidance_end: float | None = None
    clip_skip: int | None = None


class AIModelUserInput(BaseModel):
    name: str
    path: str
    path_type: PathType
    variant: Variant
    model_type: AIModelType
    model_base: AIModelBase
    control_net_type: ControlNetType | None = Field(default=None)
    tags: str = Field(default="")
    trigger_pos_words: str = Field(default="")
    trigger_neg_words: str = Field(default="")
