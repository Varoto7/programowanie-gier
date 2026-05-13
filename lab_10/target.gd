extends Node3D

func _ready() -> void:
	$Area3D.area_entered.connect(_on_hit)

func _on_hit(_area: Area3D) -> void:
	print("trafiony!")
	
	var main_node = get_tree().current_scene
	if main_node.has_method("add_score"):
		main_node.add_score()
		
	queue_free() 
