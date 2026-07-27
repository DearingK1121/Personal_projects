extends Control
#
func _ready():
	visible = false
 #
#
func show_menu():
	var gm = get_node("/root/Game/GlobalManager")
	gm.game_over = false

	# Move menu to camera center
	var camera = get_viewport().get_camera_2d()
	if camera:
		global_position = camera.get_screen_center_position()
	visible = true
	get_tree().paused = true

func _on_RestartButton_pressed():
	get_tree().paused = true
	get_tree().reload_current_scene()

func _on_QuitButton_pressed():
	get_tree().quit()
