/**
 * Exact page paths where in-body links should **not** open the side panel
 * and should **not** show the hover popover. Full-page navigation only.
 *
 * Match is exact after stripping a trailing slash — not a prefix match.
 * Add paths here when you want the same behavior on another page.
 */
export const NO_PANEL_PATHS: readonly string[] = [
	// nix.dev section indexes / hubs
	'/pages/nix-dev',
	'/pages/nix-dev/tutorials',
	'/pages/nix-dev/guides',
	'/pages/nix-dev/reference',
	'/pages/nix-dev/concepts',
	'/pages/nix-dev/contributing',
	'/pages/nix-dev/first-steps',
	'/pages/nix-dev/tutorials/first-steps',
	'/pages/nix-dev/tutorials/module-system',
	'/pages/nix-dev/tutorials/nixos',
	'/pages/nix-dev/guides/recipes',
	// Nix manual table of contents only (exact — not children)
	'/pages/nix-manual'
];

function normPath(p: string): string {
	return p.replace(/\/$/, '') || '/';
}

const noPanelSet = new Set(NO_PANEL_PATHS.map(normPath));

/** True if this pathname is listed in NO_PANEL_PATHS (exact match). */
export function isNoPanelPath(pathname: string): boolean {
	return noPanelSet.has(normPath(pathname));
}
