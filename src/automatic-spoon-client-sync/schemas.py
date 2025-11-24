from pydantic import BaseModel, Field

from .enums import (
    AIModelBase,
    AIModelStatus,
    AIModelType,
    ControlNetType,
    FileImageType,
    GeneratorStatus,
    JobStatus,
    LongPromptTechnique,
    PathType,
    Scheduler,
    Variant,
)


class GPUSchema(BaseModel):
    id: int
    name: str
    total_vram_gb: float


class InfoSchema(BaseModel):
    db_path: str
    images_path: str
    hugging_face_path: str


class AIModelSchema(BaseModel):
    id: int | None = Field(default=None)
    name: str
    status: AIModelStatus
    path: str
    path_type: PathType
    variant: Variant
    model_type: AIModelType
    model_base: AIModelBase
    tags: str
    control_net_type: ControlNetType | None = Field(default=None)
    trigger_pos_words: str | None = Field(default=None)
    trigger_neg_words: str | None = Field(default=None)
    error: str | None = Field(default=None)


class LoraAndWeight(BaseModel):
    aimodel: AIModelSchema
    weight: float


class EngineSchema(BaseModel):
    id: int | None = Field(default=None)
    name: str
    checkpoint_model: AIModelSchema
    lora_models: list[LoraAndWeight]
    control_net_models: list[AIModelSchema]
    embedding_models: list[AIModelSchema]
    scheduler: Scheduler
    guidance_scale: float
    seed: int
    width: int
    height: int
    steps: int
    long_prompt_technique: LongPromptTechnique | None = None
    vae_model: AIModelSchema | None = None
    controlnet_conditioning_scale: float | None = None
    control_guidance_start: float | None = None
    control_guidance_end: float | None = None
    clip_skip: int | None = None


class GeneratorSchema(BaseModel):
    id: int | None = Field(default=None)
    name: str
    gpu_id: int = Field(default=0)
    engine: EngineSchema
    status: GeneratorStatus


class ControlNetImageSchema(BaseModel):
    aimodel: AIModelSchema | None
    image_file_path: str
    controlnet_conditioning_scale: float


class ImageSchema(BaseModel):
    id: int | None
    job_id: int
    generator_id: int
    prompt: str
    negative_prompt: str
    ready: bool
    file_path: str
    seed: int | None = Field(default=None)
    guidance_scale: float | None = Field(default=None)
    width: int | None = Field(default=None)
    height: int | None = Field(default=None)
    steps: int | None = Field(default=None)
    control_images: list[ControlNetImageSchema] = Field(default=[])
    file_type: FileImageType = Field(default=FileImageType.PNG)
    control_guidance_start: float | None = None
    control_guidance_end: float | None = None


class JobSchema(BaseModel):
    id: int | None
    generator_id: int
    images: list[ImageSchema]
    status: JobStatus
