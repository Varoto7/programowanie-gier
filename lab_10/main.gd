extends Node3D

var score: int = 0

func add_score() -> void:
	score += 1
	print("Wynik: ", score)
