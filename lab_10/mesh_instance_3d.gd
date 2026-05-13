extends MeshInstance3D

const LIMIT_X = 5.0
const LIMIT_Y = 3.0
var speed: float = 10.0

@export var bullet_scene: PackedScene
var _shoot_cooldown: float = 0.0

func _process(delta: float) -> void:
	var direction_x = Input.get_axis("ui_left", "ui_right")
	var direction_y = Input.get_axis("ui_down", "ui_up")

	position.x += direction_x * speed * delta
	position.y += direction_y * speed * delta

	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)
	
	_shoot_cooldown -= delta
	if Input.is_action_pressed("ui_accept") and _shoot_cooldown <= 0.0:
		_shoot_cooldown = 0.3
		shoot()

func shoot() -> void:
	if bullet_scene != null:
		var bullet = bullet_scene.instantiate()
		get_tree().root.add_child(bullet)
		bullet.global_position = global_position
