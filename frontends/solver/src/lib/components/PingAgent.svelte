<script>
	let userMsg = '';
	const AGENT_WS = 'http://localhost:5556';

	function handlePing() {
		const ws = new WebSocket(AGENT_WS);

		ws.onopen = () => {
			ws.send(userMsg);
			ws.close();
		};

		ws.onclose = () => {
			console.log('WebSocket disconnected');
		};
	}
</script>

<main>
	<div class="flex">
		<input type="text" bind:value={userMsg} placeholder="Ping agent..." style="width: 100%;" />
		<button type="button" class="btn-sm variant-ghost-surface" on:click={handlePing}>Ping</button>
	</div>
</main>

<style>
	input {
		margin-bottom: 10px;
		padding: 5px;
		background-color: black;
		border-radius: 4px;
	}
	button {
		padding: 5px 10px;
		cursor: pointer;
		height: 35px;
	}
</style>
