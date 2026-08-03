/**
 * Global settings modal open state (Notion-style overlay).
 * Open from nav, command palette, home cards, or /settings.
 */

export type SettingsTab = 'appearance' | 'text' | 'editor';

class SettingsUi {
	open = $state(false);
	tab = $state<SettingsTab>('appearance');

	show(tab?: SettingsTab) {
		if (tab) this.tab = tab;
		this.open = true;
	}

	hide() {
		this.open = false;
	}

	toggle(tab?: SettingsTab) {
		if (this.open && (!tab || tab === this.tab)) {
			this.open = false;
			return;
		}
		if (tab) this.tab = tab;
		this.open = true;
	}
}

export const settingsUi = new SettingsUi();
