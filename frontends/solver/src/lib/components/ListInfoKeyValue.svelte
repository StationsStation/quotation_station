<script>
	// @ts-nocheck

	import { onMount } from 'svelte';

	export let name = 'Interface';
	let agentInfo = {};

	async function fetchData() {
		try {
			const response = await fetch('http://localhost:5555/api/agent-info');
			agentInfo = await response.json();
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	function processKey(key) {
		return key?.replace('-', ' ')?.replace('_', ' ');
	}
	onMount(() => {
		fetchData();
		const interval = setInterval(fetchData, 30000);
		return () => clearInterval(interval);
	});
</script>

<div class="section">
	<h1>{name}</h1>
	<ul class="list">
		{#each Object.keys(agentInfo) as key}
			<li>
				<span class="key">{processKey(key)}: </span>
				<span class="flex-auto value">{agentInfo[key] || 'N/A'}</span>
			</li>
		{/each}
	</ul>
</div>

<style>
	.section {
		background-color: #1a1a1a;
		border: 2px solid #30e9ff;
		border-radius: 10px;
		padding: 20px;
		box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
		width: 100%;
		height: 100%;
	}

	h1 {
		text-align: center;
		color: #30e9ff;
		text-transform: uppercase;
		letter-spacing: 2px;
		margin-bottom: 20px;
	}

	ul {
		width: 100%;
		border-collapse: separate;
		border-spacing: 0 10px;
		height: auto;
	}

	li {
		padding: 10px;
		text-align: left;
		border-bottom: 0.5px solid #00ff4178;
	}

	.key {
		color: #9af0ab;
		text-transform: uppercase;
		font-size: 12px;
	}
	.value {
		font-size: 75%;
	}
</style>
