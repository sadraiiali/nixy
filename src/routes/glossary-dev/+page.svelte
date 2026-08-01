<script lang="ts">
	import Icon from '$lib/components/Icon.svelte';
	import { canEditGlossary, isWebxdc } from '$lib/webxdc';
	import { untrack } from 'svelte';
	import type { PageData } from './$types';

	type Status = 'pending' | 'approved' | 'skipped';
	type Entry = {
		term: string;
		suggestion: string;
		translation: string;
		notes: string;
		sources: string[];
		count: number;
		is_tech: boolean;
		status: Status;
	};

	type Filter =
		| 'pending'
		| 'approved'
		| 'skipped'
		| 'tech'
		| 'filled'
		| 'empty'
		| 'multi'
		| 'differs'
		| 'notes'
		| 'all';

	type SortKey = 'term' | 'count' | 'status' | 'sources';

	let { data }: { data: PageData } = $props();

	/** Review/edit tool — only writable on Vite dev (see canEditGlossary). */
	const editable = canEditGlossary;

	// One-time snapshot of server data (edit buffer); untrack avoids state_referenced_locally
	let entries = $state<Entry[]>(
		untrack(() => structuredClone(data.glossary.entries) as Entry[])
	);
	// Prefer pending queue when editing; otherwise approved snapshot.
	let filter = $state<Filter>(untrack(() => (editable ? 'pending' : 'approved')));
	let sourceFilter = $state<string>('');
	let q = $state('');
	let sortKey = $state<SortKey>(untrack(() => (editable ? 'count' : 'term')));
	let sortDir = $state<'asc' | 'desc'>(untrack(() => (editable ? 'desc' : 'asc')));
	let showNotes = $state(untrack(() => editable));
	let dense = $state(true);
	let saving = $state(false);
	let dirty = $state(false);
	let message = $state('');
	let errorMsg = $state('');
	let lastSavedAt = $state<string | null>(null);
	let focusTerm = $state<string | null>(null);

	const statusRank: Record<Status, number> = { pending: 0, approved: 1, skipped: 2 };

	function markDirty() {
		if (!editable) return;
		dirty = true;
		message = '';
	}

	const live = $derived.by(() => {
		const tech = entries.filter((e) => e.is_tech);
		const approved = tech.filter((e) => e.status === 'approved').length;
		const pending = tech.filter((e) => e.status === 'pending').length;
		const skipped = tech.filter((e) => e.status === 'skipped').length;
		const filled = tech.filter((e) => e.translation.trim()).length;
		const empty = tech.filter((e) => !e.translation.trim() && e.status === 'pending').length;
		const multi = tech.filter((e) => e.term.includes(' ')).length;
		const differs = tech.filter(
			(e) => e.translation.trim() && e.suggestion.trim() && e.translation !== e.suggestion
		).length;
		const readyPct = tech.length ? Math.round((approved / tech.length) * 100) : 0;
		return { tech: tech.length, approved, pending, skipped, filled, empty, multi, differs, readyPct };
	});

	const sourceList = $derived.by(() => {
		const map = new Map<string, number>();
		for (const e of entries) {
			if (!e.is_tech) continue;
			for (const s of e.sources || []) {
				map.set(s, (map.get(s) || 0) + 1);
			}
		}
		return [...map.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
	});

	const filtered = $derived.by(() => {
		const query = q.trim().toLowerCase();
		let list = entries.filter((e) => {
			if (sourceFilter && !(e.sources || []).includes(sourceFilter)) return false;

			switch (filter) {
				case 'pending':
					if (!e.is_tech || e.status !== 'pending') return false;
					break;
				case 'approved':
					if (e.status !== 'approved') return false;
					break;
				case 'skipped':
					if (e.status !== 'skipped') return false;
					break;
				case 'tech':
					if (!e.is_tech) return false;
					break;
				case 'filled':
					if (!e.translation.trim()) return false;
					break;
				case 'empty':
					if (e.translation.trim() || e.status !== 'pending') return false;
					break;
				case 'multi':
					if (!e.term.includes(' ')) return false;
					break;
				case 'differs':
					if (
						!(
							e.translation.trim() &&
							e.suggestion.trim() &&
							e.translation !== e.suggestion
						)
					)
						return false;
					break;
				case 'notes':
					if (!e.notes?.trim()) return false;
					break;
				case 'all':
					break;
			}

			if (query) {
				const hay =
					`${e.term} ${e.suggestion} ${e.translation} ${e.notes} ${(e.sources || []).join(' ')}`.toLowerCase();
				if (!hay.includes(query)) return false;
			}
			return true;
		});

		list = [...list].sort((a, b) => {
			let cmp = 0;
			if (sortKey === 'term') cmp = a.term.localeCompare(b.term);
			else if (sortKey === 'count') cmp = a.count - b.count;
			else if (sortKey === 'status') cmp = statusRank[a.status] - statusRank[b.status];
			else if (sortKey === 'sources')
				cmp = (a.sources?.length || 0) - (b.sources?.length || 0);
			return sortDir === 'asc' ? cmp : -cmp;
		});
		return list;
	});

	function setFilter(f: Filter) {
		filter = f;
	}

	function toggleSort(key: SortKey) {
		if (sortKey === key) sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		else {
			sortKey = key;
			sortDir = key === 'term' ? 'asc' : 'desc';
		}
	}

	function useSuggestion(e: Entry) {
		if (e.suggestion) {
			e.translation = e.suggestion;
			if (e.status === 'skipped') e.status = 'pending';
			markDirty();
		}
	}

	function approve(e: Entry) {
		if (!e.translation.trim() && e.suggestion) e.translation = e.suggestion;
		e.status = 'approved';
		markDirty();
	}

	function skip(e: Entry) {
		e.status = 'skipped';
		markDirty();
	}

	function setPending(e: Entry) {
		e.status = 'pending';
		markDirty();
	}

	function applySuggestionAll() {
		let n = 0;
		for (const e of entries) {
			if (e.is_tech && !e.translation.trim() && e.suggestion && e.status === 'pending') {
				e.translation = e.suggestion;
				n++;
			}
		}
		markDirty();
		message = `${n} پیشنهاد خالی کپی شد، ذخیره کنید.`;
	}

	function approveAllFilled() {
		let n = 0;
		for (const e of entries) {
			if (e.translation.trim() && e.status !== 'approved') {
				e.status = 'approved';
				n++;
			}
		}
		markDirty();
		message = `${n} مورد تأیید شد، ذخیره کنید.`;
	}

	function approveVisible() {
		let n = 0;
		for (const e of filtered) {
			if (!e.translation.trim() && e.suggestion) e.translation = e.suggestion;
			if (e.translation.trim()) {
				e.status = 'approved';
				n++;
			}
		}
		markDirty();
		message = `${n} موردِ نمایش‌داده‌شده تأیید شد، ذخیره کنید.`;
	}

	function skipVisibleEmpty() {
		let n = 0;
		for (const e of filtered) {
			if (!e.translation.trim()) {
				e.status = 'skipped';
				n++;
			}
		}
		markDirty();
		message = `${n} مورد بدون ترجمه رد شد، ذخیره کنید.`;
	}

	async function save() {
		if (!editable) return;
		saving = true;
		message = '';
		errorMsg = '';
		try {
			const res = await fetch('/api/glossary', {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					version: data.glossary.version,
					docs: data.glossary.docs,
					entries
				})
			});
			if (!res.ok) throw new Error((await res.text()) || res.statusText);
			const body = await res.json();
			dirty = false;
			lastSavedAt = new Date().toLocaleTimeString('fa-IR');
			message = `ذخیره شد · ${body.count} واژه · فقط «تأیید»ها در translate-docs می‌روند`;
		} catch (err) {
			errorMsg = err instanceof Error ? err.message : String(err);
		} finally {
			saving = false;
		}
	}

	function onKey(e: KeyboardEvent) {
		if (!editable) return;
		if ((e.ctrlKey || e.metaKey) && e.key === 's') {
			e.preventDefault();
			void save();
		}
	}

	function shortDoc(name: string) {
		return name.replace(/\.md$/i, '').replace(/^towards-reproducibility-/, 'pin-');
	}

	function statusLabel(s: Status) {
		if (s === 'approved') return 'تأیید';
		if (s === 'skipped') return 'رد';
		return 'انتظار';
	}
</script>

<svelte:window onkeydown={onKey} />

<svelte:head>
	<title>واژه‌نامه · ویرایش · {live.approved}/{live.tech} تأیید</title>
	<meta name="robots" content="noindex,nofollow" />
</svelte:head>

<section class="g" class:g--dense={dense} class:g--readonly={!editable}>
	<div class="g-top">
		<div class="g-top__title">
			<h1>واژه‌نامه · ویرایش</h1>
			<span class="g-pill g-pill--muted" dir="ltr">/glossary-dev</span>
			<span class="g-pill g-pill--muted" dir="ltr">v{data.glossary.version}</span>
			{#if editable}
				<span class="g-pill g-pill--ok">حالت ویرایش · dev</span>
				{#if dirty}
					<span class="g-pill g-pill--warn">ذخیره‌نشده</span>
				{:else if lastSavedAt}
					<span class="g-pill g-pill--ok">ذخیره {lastSavedAt}</span>
				{/if}
			{:else}
				<span class="g-pill g-pill--muted">{isWebxdc ? 'فقط‌خواندنی · Webxdc' : 'فقط‌خواندنی'}</span>
			{/if}
		</div>
		{#if editable}
			<p class="g-top__hint">
				ابزار داخلی تأیید واژه‌ها · فقط وضعیت <strong>تأیید</strong> به
				<code dir="ltr">translate-docs</code> می‌رود ·
				<code dir="ltr">Ctrl+S</code> ذخیره · واژه‌نامهٔ عمومی:
				<a href="/glossary" dir="ltr">/glossary</a>
			</p>
		{:else}
			<p class="g-top__hint">
				ویرایش فقط با <code dir="ltr">npm run dev</code>. واژه‌نامهٔ نهایی:
				<a href="/glossary">/glossary</a>
			</p>
		{/if}
	</div>

	{#if editable}
		<!-- Metric strip (dev review) -->
		<div class="g-metrics" role="group" aria-label="آمار زنده">
			<button
				type="button"
				class="g-metric"
				class:is-active={filter === 'tech'}
				onclick={() => setFilter('tech')}
			>
				<span class="g-metric__n">{live.tech}</span>
				<span class="g-metric__l">تخصصی</span>
			</button>
			<button
				type="button"
				class="g-metric g-metric--pending"
				class:is-active={filter === 'pending'}
				onclick={() => setFilter('pending')}
			>
				<span class="g-metric__n">{live.pending}</span>
				<span class="g-metric__l">انتظار</span>
			</button>
			<button
				type="button"
				class="g-metric g-metric--ok"
				class:is-active={filter === 'approved'}
				onclick={() => setFilter('approved')}
			>
				<span class="g-metric__n">{live.approved}</span>
				<span class="g-metric__l">تأیید</span>
			</button>
			<button
				type="button"
				class="g-metric g-metric--skip"
				class:is-active={filter === 'skipped'}
				onclick={() => setFilter('skipped')}
			>
				<span class="g-metric__n">{live.skipped}</span>
				<span class="g-metric__l">رد</span>
			</button>
			<button
				type="button"
				class="g-metric"
				class:is-active={filter === 'filled'}
				onclick={() => setFilter('filled')}
			>
				<span class="g-metric__n">{live.filled}</span>
				<span class="g-metric__l">پر</span>
			</button>
			<button
				type="button"
				class="g-metric"
				class:is-active={filter === 'empty'}
				onclick={() => setFilter('empty')}
			>
				<span class="g-metric__n">{live.empty}</span>
				<span class="g-metric__l">خالی</span>
			</button>
			<button
				type="button"
				class="g-metric"
				class:is-active={filter === 'multi'}
				onclick={() => setFilter('multi')}
			>
				<span class="g-metric__n">{live.multi}</span>
				<span class="g-metric__l">چندکلمه‌ای</span>
			</button>
			<button
				type="button"
				class="g-metric"
				class:is-active={filter === 'differs'}
				onclick={() => setFilter('differs')}
			>
				<span class="g-metric__n">{live.differs}</span>
				<span class="g-metric__l">≠ پیشنهاد</span>
			</button>
			<div class="g-metric g-metric--progress" title="درصد تأیید نسبت به تخصصی">
				<div class="g-progress">
					<div class="g-progress__bar" style="width: {live.readyPct}%"></div>
				</div>
				<span class="g-metric__n">{live.readyPct}%</span>
				<span class="g-metric__l">آماده</span>
			</div>
		</div>

		<div class="g-sources">
			<span class="g-sources__label">منبع:</span>
			<button
				type="button"
				class="g-chip"
				class:is-active={!sourceFilter}
				onclick={() => (sourceFilter = '')}
			>
				همه
			</button>
			{#each sourceList as [src, n] (src)}
				<button
					type="button"
					class="g-chip"
					class:is-active={sourceFilter === src}
					title={src}
					onclick={() => (sourceFilter = sourceFilter === src ? '' : src)}
				>
					<span dir="ltr">{shortDoc(src)}</span>
					<span class="g-chip__n">{n}</span>
				</button>
			{/each}
		</div>
	{:else}
		<!-- compact stats for read-only -->
		<div class="g-metrics g-metrics--ro" role="group" aria-label="آمار">
			<div class="g-metric">
				<span class="g-metric__n">{live.approved}</span>
				<span class="g-metric__l">تأیید</span>
			</div>
			<div class="g-metric">
				<span class="g-metric__n">{live.tech}</span>
				<span class="g-metric__l">تخصصی</span>
			</div>
			<div class="g-metric g-metric--progress">
				<div class="g-progress">
					<div class="g-progress__bar" style="width: {live.readyPct}%"></div>
				</div>
				<span class="g-metric__n">{live.readyPct}%</span>
				<span class="g-metric__l">پوشش</span>
			</div>
		</div>
	{/if}

	<div class="g-bar">
		<input
			class="g-bar__search"
			type="search"
			placeholder={editable ? 'جستجو: term · ترجمه · note · فایل…' : 'جستجو در واژه‌نامه…'}
			bind:value={q}
		/>
		{#if editable}
			<label class="g-bar__check">
				<input type="checkbox" bind:checked={showNotes} />
				یادداشت
			</label>
			<label class="g-bar__check">
				<input type="checkbox" bind:checked={dense} />
				فشرده
			</label>
			<div class="g-bar__actions">
				<button type="button" class="g-btn" onclick={applySuggestionAll}>کپی پیشنهاد خالی</button>
				<button type="button" class="g-btn" onclick={approveAllFilled}>تأیید همهٔ پر</button>
				<button type="button" class="g-btn" onclick={approveVisible}>تأییدِ نمایش</button>
				<button type="button" class="g-btn" onclick={skipVisibleEmpty}>ردِ خالی‌های نمایش</button>
				<button
					type="button"
					class="g-btn g-btn--primary"
					onclick={save}
					disabled={saving || !dirty}
				>
					{saving ? '…' : dirty ? 'ذخیره *' : 'ذخیره'}
				</button>
			</div>
		{:else}
			<div class="g-bar__actions">
				<button
					type="button"
					class="g-btn"
					class:is-active={filter === 'approved'}
					onclick={() => setFilter('approved')}
				>
					تأیید‌شده
				</button>
				<button
					type="button"
					class="g-btn"
					class:is-active={filter === 'tech'}
					onclick={() => setFilter('tech')}
				>
					همهٔ تخصصی
				</button>
			</div>
		{/if}
	</div>

	{#if editable}
		{#if message}
			<div class="g-flash g-flash--ok" role="status">{message}</div>
		{/if}
		{#if errorMsg}
			<div class="g-flash g-flash--err" role="alert">{errorMsg}</div>
		{/if}
	{/if}

	<div class="g-meta-row">
		<span
			>{filtered.length} ردیف · مرتب:
			<button type="button" class="g-link" onclick={() => toggleSort('term')}
				>az{sortKey === 'term' ? (sortDir === 'desc' ? '↓' : '↑') : ''}</button
			>
			·
			<button type="button" class="g-link" onclick={() => toggleSort('count')}
				>freq{sortKey === 'count' ? (sortDir === 'desc' ? '↓' : '↑') : ''}</button
			>
		</span>
		{#if editable}
			<span class="g-meta-row__hint" dir="ltr">make translate-docs</span>
		{/if}
	</div>

	<div class="g-table-wrap">
		<table class="g-table">
			<thead>
				<tr>
					<th class="c-idx">#</th>
					<th class="c-term">
						<button type="button" class="g-th" onclick={() => toggleSort('term')}>EN</button>
					</th>
					{#if editable}
						<th class="c-freq">
							<button type="button" class="g-th" onclick={() => toggleSort('count')}>×</button>
						</th>
						<th class="c-lex">lexicon</th>
						<th class="c-tr">FA / شما</th>
						<th class="c-st">وضعیت</th>
						<th class="c-src">منابع</th>
						<th class="c-act">اقدام</th>
					{:else}
						<th class="c-tr">فارسی</th>
						<th class="c-freq">
							<button type="button" class="g-th" onclick={() => toggleSort('count')}>×</button>
						</th>
					{/if}
				</tr>
			</thead>
			<tbody>
				{#each filtered as e, i (e.term)}
					{@const differs =
						e.translation.trim() &&
						e.suggestion.trim() &&
						e.translation !== e.suggestion}
					{@const multi = e.term.includes(' ')}
					<tr
						class:row-ok={e.status === 'approved'}
						class:row-skip={e.status === 'skipped'}
						class:row-focus={editable && focusTerm === e.term}
						class:row-diff={editable && differs}
					>
						<td class="c-idx" dir="ltr">{i + 1}</td>
						<td class="c-term" dir="ltr">
							<code class="term-code">{e.term}</code>
							{#if multi && editable}<span class="tag tag-mw">MW</span>{/if}
						</td>
						{#if editable}
							<td class="c-freq" dir="ltr">{e.count}</td>
							<td class="c-lex" dir="auto">
								<span class="lex-text" title={e.suggestion || ''}>{e.suggestion || '·'}</span>
								{#if e.suggestion && e.translation !== e.suggestion}
									<button
										type="button"
										class="g-mini"
										title="کپی پیشنهاد lexicon"
										onclick={() => useSuggestion(e)}>↩</button
									>
								{/if}
							</td>
							<td class="c-tr">
								<input
									class="tr-input"
									class:tr-diff={differs}
									type="text"
									dir="auto"
									bind:value={e.translation}
									oninput={markDirty}
									onfocus={() => (focusTerm = e.term)}
									placeholder="ترجمه…"
									aria-label={`ترجمه ${e.term}`}
								/>
								{#if showNotes}
									<input
										class="note-input"
										type="text"
										dir="auto"
										bind:value={e.notes}
										oninput={markDirty}
										placeholder="یادداشت / API note…"
										aria-label={`یادداشت ${e.term}`}
									/>
								{/if}
							</td>
							<td class="c-st">
								<div class="st-group" role="group" aria-label={`وضعیت ${e.term}`}>
									<button
										type="button"
										class="st"
										class:st--on={e.status === 'pending'}
										class:st--pending={e.status === 'pending'}
										onclick={() => setPending(e)}
										title="در انتظار">…</button
									>
									<button
										type="button"
										class="st"
										class:st--on={e.status === 'approved'}
										class:st--ok={e.status === 'approved'}
										onclick={() => approve(e)}
										title="تأیید"
										><Icon name="check" size={14} /></button
									>
									<button
										type="button"
										class="st"
										class:st--on={e.status === 'skipped'}
										class:st--skip={e.status === 'skipped'}
										onclick={() => skip(e)}
										title="رد"
										><Icon name="x" size={14} /></button
									>
								</div>
								<span class="st-label">{statusLabel(e.status)}</span>
							</td>
							<td class="c-src">
								<div class="src-list">
									{#each e.sources || [] as s}
										<span class="src-chip" dir="ltr" title={s}>{shortDoc(s)}</span>
									{/each}
								</div>
							</td>
							<td class="c-act">
								<button type="button" class="g-mini g-mini--ok" onclick={() => approve(e)} title="تأیید">
									<Icon name="check" size={14} />
								</button>
								<button type="button" class="g-mini" onclick={() => useSuggestion(e)} title="lexicon">
									L
								</button>
								<button type="button" class="g-mini g-mini--skip" onclick={() => skip(e)} title="رد">
									<Icon name="x" size={14} />
								</button>
							</td>
						{:else}
							<td class="c-tr c-tr--ro" dir="auto">
								{e.translation || e.suggestion || '—'}
							</td>
							<td class="c-freq" dir="ltr">{e.count}</td>
						{/if}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	{#if filtered.length === 0}
		<p class="g-empty">هیچ ردیفی با این فیلتر/جستجو نیست.</p>
	{/if}
</section>
