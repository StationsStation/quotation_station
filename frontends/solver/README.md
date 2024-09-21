# create-svelte

Everything you need to build a Svelte project, powered by [`create-svelte`](https://github.com/sveltejs/kit/tree/main/packages/create-svelte).

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

Renders componetns on the dashboard using coordinates and component name.

<b>Params</b>

fixed: boolean - is component draggable 
canRemove: boolean - enables removing component from the dashboard
com: components name - currently supports ListInfoKeyValue, GrafanaDashboard, WebSocketData, PingAgent, WalletConnect

------------------------------------

ListInfoKeyValue: fetches data from an endpoint and renders agent info as a key value pair
GrafanaDashboard: provides input for a custom grafana dashboard and renders a dashboard
WebSocketData: renders websocket data using agent endpoint
PingAgent: input for pinging an agent
WalletConnect: provides web3 wallet connection

----------------------------------
Data example 
( x axis devided into 6 columns )
w = width
h = height

```
// example
        [{
            coordinates: {
                x: 0,
                y: 4,
                w: 6,
                h: 3
            },
            com: 'GrafanaDashboard',
            fixed: false, 
            canRemove: true
        }]
```
