extends Control

var has_already_started := false

func _ready():
	if has_already_started:
		visible = false
		get_tree().paused = false
	else:
		print("Start Menu Ready")
		get_tree().paused = true
		visible = true
		has_already_started = true


func _on_StartButton_pressed():
	print("Start button was pressed!")
	get_tree().change_scene_to_file("res://Scenes/Game.tscn")

func _on_QuitButton_pressed():
	get_tree().quit()
