from tv_remote import TVRemote
import sys

def main():
    remote = TVRemote()
    
    try:
        remote.connect()
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("\n" + "="*50)
    print("🎮 LG WebOS TV Remote Control")
    print("="*50)
    print("\nCommands:")
    print("  Volume: vol+ vol- mute vol:50")
    print("  Navigation: up down left right ok back home")
    print("  Playback: play pause")
    print("  Channel: ch+ ch-")
    print("  App: app:netflix app:youtube app:disney")
    print("  Notification: notify:Hello")
    print("  Exit: exit, quit, q")
    print("="*50 + "\n")

    while True:
        try:
            command = input("🎮 Command: ").strip().lower()
            
            if command in ['exit', 'quit', 'q']:
                print("👋 Exiting...")
                break
            
            elif command == 'vol+':
                remote.volume_up()
            elif command == 'vol-':
                remote.volume_down()
            elif command == 'mute':
                remote.mute()
            elif command.startswith('vol:'):
                level = int(command.split(':')[1])
                remote.set_volume(level)
            
            elif command == 'up':
                remote.arrow_up()
            elif command == 'down':
                remote.arrow_down()
            elif command == 'left':
                remote.arrow_left()
            elif command == 'right':
                remote.arrow_right()
            elif command == 'ok':
                remote.ok()
            elif command == 'back':
                remote.back()
            elif command == 'home':
                remote.home()
            
            elif command == 'play':
                remote.play()
            elif command == 'pause':
                remote.pause()
            
            elif command == 'ch+':
                remote.channel_up()
            elif command == 'ch-':
                remote.channel_down()
            
            elif command.startswith('app:'):
                app = command.split(':')[1]
                remote.launch_app(app)
            
            elif command.startswith('notify:'):
                message = command.split(':', 1)[1]
                remote.notify(message)
            
            else:
                print("❌ Unknown command! Type 'help'.")
        
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
