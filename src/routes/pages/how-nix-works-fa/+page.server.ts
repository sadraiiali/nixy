import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

/** مسیر قدیمی → راهنمای فارسی اصلی */
export const load: PageServerLoad = () => {
	redirect(301, '/pages/how-nix-works');
};
