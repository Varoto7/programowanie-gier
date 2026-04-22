extends PathFollow3D

@export var rail_speed: float = 0.02

func _ready() -> void:
	pass 

func _process(delta: float) -> void:
	progress_ratio += rail_speed * delta
