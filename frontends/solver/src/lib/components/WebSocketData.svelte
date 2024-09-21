<script>
	// @ts-nocheck

	import { onMount } from 'svelte';

	export let AGENT_WS = 'http://localhost:5556';

	let data = [];
	let filteredData = [];
	let isExpanded = false;
	let filter = '';

	onMount(() => {
		const ws = new WebSocket(AGENT_WS);

		ws.onopen = () => {
			console.log('WebSocket connected');
		};

		ws.onmessage = (message) => {
			const newItem = { text: message.data, expanded: isExpanded };
			data = [newItem, ...data];
			applyFilter();
		};

		ws.onclose = () => {
			console.log('WebSocket disconnected');
		};

		return () => {
			ws.close();
		};
	});

	function toggleExpand(index) {
		filteredData = filteredData.map((item, i) =>
			i === index ? { ...item, expanded: !item.expanded } : item
		);
	}

	function toggleExpandAll() {
		isExpanded = !isExpanded;
		filteredData = filteredData.map((item) => ({ ...item, expanded: isExpanded }));
	}

	function applyFilter() {
		if (filter) {
			filteredData = data.filter((item) => item.text.includes(filter));
		} else {
			filteredData = [...data];
		}
	}

	function setFilter(newFilter) {
		filter = newFilter;
		applyFilter();
	}
</script>

<main>
	<div class="data-container">
		<h2>WebSocket Data Stream</h2>
		<div class="btn-group variant-filled mb-2">
			<button class="expand-button" on:click={toggleExpandAll}
				>{isExpanded ? 'Collapse All' : 'Expand All'}</button
			>
			<button on:click={() => setFilter('')}>All</button>
			<button class:selected={filter === '[INFO]'} on:click={() => setFilter('[INFO]')}>INFO</button
			>
			<button class:selected={filter === '[ERROR]'} on:click={() => setFilter('[ERROR]')}
				>ERROR</button
			>
			<button class:selected={filter === '[WARNING]'} on:click={() => setFilter('[WARNING]')}
				>WARNING</button
			>
		</div>
		{#if filteredData.length > 0}
			<ul>
				{#each filteredData as { text, expanded }, index}
					<li>
						<div class="item-header" on:click={() => toggleExpand(index)}>
							{#if text.length > 150}
								<span class="arrow">{expanded ? '▼' : '▶'}</span>
							{/if}
							<span class="text">
								{#if expanded}
									<div class="expanded">{text}</div>
								{:else}
									{text.slice(0, 150)}{text.length > 150 ? '...' : ''}
								{/if}
							</span>
						</div>
					</li>
				{/each}
			</ul>
		{:else}
			<p>No data available</p>
		{/if}
	</div>
</main>

<style>
	:global(body) {
		background-color: #0a0a0a;
		color: #30e9ff;
		font-family: 'Courier New', monospace;
	}

	h2 {
		text-align: center;
		color: #30e9ff;
		text-transform: uppercase;
		letter-spacing: 2px;
		margin-bottom: 20px;
	}

	.data-container {
		background: linear-gradient(135deg, rgba(10, 10, 10, 0.9) 0%, rgba(20, 20, 20, 0.8) 100%);
		border: 2px solid #30e9ff;
		border-radius: 10px;
		padding: 20px;
		box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
		max-height: 90vh;
		overflow-y: auto;
	}

	ul {
		list-style-type: none;
		padding: 0;
		margin: 0;
	}

	li {
		margin-bottom: 10px;
		padding: 10px;
		border-radius: 5px;
		color: #00ff41;
		font-family: 'Courier New', monospace;
		font-size: 14px;
		transition: background 0.3s;
		background: rgba(255, 0, 255, 0.1);
		cursor: pointer;
	}

	li:hover {
		background: rgba(0, 255, 65, 0.2);
	}

	.item-header {
		display: flex;
	}

	.arrow {
		margin-right: 10px;
		color: #30e9ff;
		font-size: 14px;
	}

	.text {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		word-wrap: break-word;
	}

	li.expanded .text {
		white-space: normal;
	}

	p {
		text-align: center;
		color: #ff0000;
		font-size: 18px;
		font-family: 'Courier New', monospace;
	}
	.expanded {
		height: 100%;
		display: flex;
		flex-direction: column;
		flex-wrap: wrap;
		max-width: 90%;
		text-wrap: balance;
	}

	.btn-group {
		display: flex;
		justify-content: center;
		margin-bottom: 20px;
		background: #1d2425;
		color: white;
	}

	.btn-group button {
		margin: 0 5px;
		padding: 10px 20px;
		color: #0a0a0a;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		font-family: 'Courier New', monospace;
		font-size: 12px;
		transition: background-color 0.3s;
	}

	.btn-group button:hover {
		background-color: #00ff41;
		color: #0a0a0a;
	}

	.btn-group button.selected {
		background-color: #00ff41;
		color: #0a0a0a;
	}

	.expand-button {
		display: block;
		margin: 0 auto 20px;
		padding: 10px 20px;
		color: #0a0a0a;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		font-family: 'Courier New', monospace;
		font-size: 16px;
		transition: background-color 0.3s;
	}

	.expand-button:hover {
		background-color: #00ff41;
		color: #0a0a0a;
	}
</style>
