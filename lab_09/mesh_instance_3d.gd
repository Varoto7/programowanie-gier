extends MeshInstance3D

const LIMIT_X = 5.0
const LIMIT_Y = 3.0
var speed: float = 10.0

func _process(delta: float) -> void:
	var direction_x = Input.get_axis("ui_left", "ui_right")
	var direction_y = Input.get_axis("ui_down", "ui_up")

	position.x += direction_x * speed * delta
	position.y += direction_y * speed * delta

	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)
