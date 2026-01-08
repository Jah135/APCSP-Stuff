import keyboard
from time import sleep

class Input:
	def read(self) -> str | None:
		...

class KeyboardInput(Input):
	def __init__(self) -> None:
		self._recorded = []
		self._is_recording = False

	def start_recording(self):
		self._recorded.clear()
		self._is_recording = True

	def stop_recording(self) -> list[str]:
		self._is_recording = False
		return self._recorded

	def read(self) -> str | None:
		key = keyboard.read_key()

		if not keyboard.is_pressed(key):
			return None
		
		output_key = str(key)

		if self._is_recording:
			self._recorded.append(output_key)

		return output_key

class PlaybackInput(Input):
	def __init__(self, sequence: list[str], delay_sec: float = 0.1) -> None:
		self.sequence = sequence
		self._current_key = 0
		self._delay = delay_sec

	def read(self) -> str | None:
		sleep(self._delay)

		current_key = self.sequence[self._current_key]
		self._current_key += 1

		return current_key