// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

/** Minimal WebMCP typings (https://webmachinelearning.github.io/webmcp/) */
interface ModelContextTool {
	name: string;
	title?: string;
	description: string;
	inputSchema?: object;
	execute: (input: object) => Promise<unknown>;
	annotations?: { readOnlyHint?: boolean; untrustedContentHint?: boolean };
}

interface ModelContext extends EventTarget {
	registerTool?(
		tool: ModelContextTool,
		options?: { signal?: AbortSignal; exposedTo?: string[] }
	): Promise<void>;
	getTools?(options?: { fromOrigins?: string[] }): Promise<unknown[]>;
	provideContext?(ctx: {
		tools: Array<{
			name: string;
			description: string;
			inputSchema?: object;
			execute: (input: object) => Promise<unknown>;
		}>;
	}): void | Promise<void>;
	ontoolchange?: ((this: ModelContext, ev: Event) => unknown) | null;
}

interface Document {
	readonly modelContext?: ModelContext;
}

interface Navigator {
	readonly modelContext?: ModelContext;
}

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

declare module '*?worker' {
	const workerConstructor: {
		new (options?: { name?: string }): Worker;
	};
	export default workerConstructor;
}

export {};
