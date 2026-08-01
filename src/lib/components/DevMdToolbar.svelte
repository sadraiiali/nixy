<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import {
		devMdCancel,
		devMdEdit,
		devMdRedo,
		devMdSave,
		devMdUndo
	} from '$lib/dev-md-edit.svelte';
</script>

{#if devMdEdit.open}
	<div class="dev-md-fab" data-no-panel role="toolbar" aria-label="ویرایش صفحه">
		<button
			type="button"
			class="dev-md-fab__btn dev-md-fab__btn--save"
			disabled={devMdEdit.saving || !devMdEdit.dirty}
			onclick={() => void devMdSave()}
			title="ذخیره (Ctrl+S)"
		>
			{#if devMdEdit.saving}
				<span class="dev-md-fab__spin" aria-hidden="true">
					<Icon name="loader-circle" size={18} />
				</span>
			{:else}
				<Icon name="save" size={18} />
			{/if}
			<span class="dev-md-fab__label">ذخیره</span>
			{#if devMdEdit.dirty}
				<span class="dev-md-fab__badge" aria-hidden="true"></span>
			{/if}
		</button>
		<div class="dev-md-fab__hist" role="group" aria-label="واگرد / ازنو">
			<button
				type="button"
				class="dev-md-fab__btn dev-md-fab__btn--hist"
				disabled={!devMdEdit.canUndo}
				onclick={() => devMdUndo()}
				title="واگرد (Ctrl+Z)"
			>
				<span class="dev-md-fab__icon" aria-hidden="true">
					<Icon name="rotate-ccw" size={16} />
				</span>
				<span class="dev-md-fab__label">واگرد</span>
			</button>
			<button
				type="button"
				class="dev-md-fab__btn dev-md-fab__btn--hist"
				disabled={!devMdEdit.canRedo}
				onclick={() => devMdRedo()}
				title="ازنو (Ctrl+Shift+Z / Ctrl+Y)"
			>
				<span class="dev-md-fab__icon dev-md-fab__icon--flip" aria-hidden="true">
					<Icon name="rotate-ccw" size={16} />
				</span>
				<span class="dev-md-fab__label">ازنو</span>
			</button>
		</div>
		<button
			type="button"
			class="dev-md-fab__btn dev-md-fab__btn--cancel"
			onclick={() => void devMdCancel()}
			title="انصراف (Esc)"
		>
			<Icon name="x" size={18} />
			<span class="dev-md-fab__label">انصراف</span>
		</button>
		{#if devMdEdit.statusMsg && !devMdEdit.dirty}
			<span class="dev-md-fab__status" title={devMdEdit.statusMsg}>
				<Icon name="check" size={14} />
				<span>ذخیره شد</span>
			</span>
		{/if}
		{#if devMdEdit.errorMsg}
			<span class="dev-md-fab__err" title={devMdEdit.errorMsg}>خطا</span>
		{/if}
	</div>
{/if}

<style>
	.dev-md-fab {
		position: fixed;
		left: max(0.65rem, env(safe-area-inset-left, 0px));
		top: 50%;
		transform: translateY(-50%);
		z-index: 95;
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0.45rem;
		padding: 0;
		margin: 0;
		border: none;
		background: transparent;
		font-family: var(--font-ui);
		/* room so labels fit */
		width: auto;
		max-width: min(7.5rem, calc(100vw - 1.2rem));
	}

	.dev-md-fab__btn {
		position: relative;
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.2rem;
		min-width: 3.35rem;
		min-height: 3.35rem;
		margin: 0;
		padding: 0.45rem 0.55rem 0.4rem;
		border: 1px solid var(--line);
		border-radius: 0.75rem;
		background: var(--bg);
		color: var(--fg);
		font-family: var(--font-ui);
		font-size: 0.72rem;
		font-weight: 700;
		line-height: 1.15;
		cursor: pointer;
		box-shadow:
			0 2px 8px color-mix(in srgb, #0f172a 10%, transparent),
			0 0 0 1px color-mix(in srgb, var(--line) 40%, transparent);
		transition:
			background 0.12s ease,
			border-color 0.12s ease,
			box-shadow 0.12s ease,
			transform 0.12s ease;
	}

	.dev-md-fab__btn:hover:not(:disabled) {
		transform: translateY(-1px);
		box-shadow:
			0 6px 16px color-mix(in srgb, #0f172a 12%, transparent),
			0 0 0 1px color-mix(in srgb, var(--accent) 25%, var(--line));
	}

	.dev-md-fab__btn:active:not(:disabled) {
		transform: translateY(0);
	}

	.dev-md-fab__btn:disabled {
		opacity: 0.45;
		cursor: not-allowed;
		box-shadow: none;
	}

	.dev-md-fab__btn--save {
		background: color-mix(in srgb, var(--accent) 16%, var(--bg));
		border-color: color-mix(in srgb, var(--accent) 42%, var(--line));
		color: var(--fg);
	}
	.dev-md-fab__btn--save:hover:not(:disabled) {
		background: color-mix(in srgb, var(--accent) 24%, var(--bg));
		border-color: color-mix(in srgb, var(--accent) 55%, var(--line));
	}
	.dev-md-fab__btn--save:disabled {
		background: var(--bg-soft);
		border-color: var(--line);
	}

	.dev-md-fab__btn--cancel {
		background: var(--bg);
		border-color: var(--line);
	}
	.dev-md-fab__btn--cancel:hover:not(:disabled) {
		background: color-mix(in srgb, #ef4444 8%, var(--bg));
		border-color: color-mix(in srgb, #ef4444 28%, var(--line));
		color: #b91c1c;
	}

	.dev-md-fab__hist {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}

	.dev-md-fab__btn--hist {
		min-width: 3.1rem;
		min-height: 2.85rem;
		padding: 0.35rem 0.45rem 0.3rem;
		font-size: 0.68rem;
	}

	.dev-md-fab__icon {
		display: inline-flex;
		line-height: 0;
	}
	.dev-md-fab__icon--flip {
		transform: scaleX(-1);
	}

	.dev-md-fab__label {
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.01em;
	}

	.dev-md-fab__badge {
		position: absolute;
		top: 0.28rem;
		inset-inline-end: 0.28rem;
		width: 0.45rem;
		height: 0.45rem;
		border-radius: 999px;
		background: #f59e0b;
		box-shadow: 0 0 0 2px color-mix(in srgb, var(--bg) 90%, transparent);
	}

	.dev-md-fab__spin {
		display: inline-flex;
		animation: dev-md-spin 0.75s linear infinite;
	}
	@keyframes dev-md-spin {
		to {
			transform: rotate(360deg);
		}
	}

	.dev-md-fab__status {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 0.25rem;
		padding: 0.25rem 0.4rem;
		border-radius: 0.45rem;
		background: color-mix(in srgb, #22c55e 12%, var(--bg));
		border: 1px solid color-mix(in srgb, #22c55e 28%, var(--line));
		color: var(--ok, #15803d);
		font-size: 0.65rem;
		font-weight: 700;
	}

	.dev-md-fab__err {
		text-align: center;
		padding: 0.25rem 0.35rem;
		border-radius: 0.45rem;
		background: color-mix(in srgb, #ef4444 12%, var(--bg));
		border: 1px solid color-mix(in srgb, #ef4444 30%, var(--line));
		color: #b91c1c;
		font-size: 0.65rem;
		font-weight: 700;
		cursor: help;
	}
</style>
