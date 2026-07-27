extends Control

func _ready():
	print("Start Menu Ready")
	get_tree().paused = true
	visible = true
	

func _on_Start_pressed():
	print("Start button was pressed!")
	get_tree().paused = false
	visible = false

func _on_Quit_pressed():
	get_tree().quit()
