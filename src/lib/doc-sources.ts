/** Original English sources this site is translated/adapted from. */

export type DocSource = {
	name: string;
	/** Canonical docs / project site */
	url: string;
	/** GitHub repository */
	git: string;
	/** Short role blurb (Persian) */
	role: string;
	/** Short license label (e.g. CC BY-SA 4.0) */
	license: string;
	/** Link to the license text / license file in the source repo */
	licenseUrl: string;
	/** Last time local FA content for this source was updated (YYYY-MM-DD) */
	updated: string;
};

export const docSources: DocSource[] = [
	{
		name: 'nix.dev',
		url: 'https://nix.dev/',
		git: 'https://github.com/NixOS/nix.dev',
		role: 'آموزش‌ها، راهنماها و مفاهیم رسمی',
		license: 'CC BY-SA 4.0',
		licenseUrl: 'https://github.com/NixOS/nix.dev/blob/master/LICENSE.md',
		updated: '2026-07-28'
	},
	{
		name: 'Nix reference manual',
		url: 'https://nix.dev/manual/nix/stable/',
		git: 'https://github.com/NixOS/nix',
		role: 'راهنمای مرجع بستهٔ Nix',
		license: 'LGPL-2.1',
		licenseUrl: 'https://github.com/NixOS/nix/blob/master/COPYING',
		updated: '2026-07-28'
	},
	{
		name: 'Nixpkgs manual',
		url: 'https://nixos.org/manual/nixpkgs/stable/',
		git: 'https://github.com/NixOS/nixpkgs',
		role: 'راهنمای مجموعهٔ بسته‌های Nix (Nixpkgs)',
		license: 'MIT',
		licenseUrl: 'https://github.com/NixOS/nixpkgs/blob/master/COPYING',
		updated: '2026-07-30'
	},
	{
		name: 'A tour of Nix',
		url: 'https://nixcloud.io/tour/',
		git: 'https://github.com/nixcloud/tour_of_nix',
		role: 'تور تعاملی زبان نیکس',
		license: 'LGPL-2.1',
		licenseUrl: 'https://github.com/nixcloud/tour_of_nix/blob/master/COPYING',
		updated: '2026-07-28'
	}
];

/** Subset commonly mentioned in the help card (matches previous copy). */
export const helpCardSources: DocSource[] = docSources.filter((s) =>
	['nix.dev', 'Nix reference manual', 'A tour of Nix'].includes(s.name)
);
