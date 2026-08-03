import arrowLeft from './lucide/arrow-left.svg?raw';
import arrowRight from './lucide/arrow-right.svg?raw';
import arrowUpRight from './lucide/arrow-up-right.svg?raw';
import ban from './lucide/ban.svg?raw';
import book from './lucide/book.svg?raw';
import bookOpen from './lucide/book-open.svg?raw';
import check from './lucide/check.svg?raw';
import chevronLeft from './lucide/chevron-left.svg?raw';
import chevronRight from './lucide/chevron-right.svg?raw';
import circleCheck from './lucide/circle-check.svg?raw';
import circleHelp from './lucide/circle-help.svg?raw';
import eye from './lucide/eye.svg?raw';
import eyeOff from './lucide/eye-off.svg?raw';
import github from './lucide/github.svg?raw';
import graduationCap from './lucide/graduation-cap.svg?raw';
import house from './lucide/house.svg?raw';
import layers from './lucide/layers.svg?raw';
import library from './lucide/library.svg?raw';
import lightbulb from './lucide/lightbulb.svg?raw';
import list from './lucide/list.svg?raw';
import loaderCircle from './lucide/loader-circle.svg?raw';
import map from './lucide/map.svg?raw';
import menu from './lucide/menu.svg?raw';
import monitor from './lucide/monitor.svg?raw';
import moon from './lucide/moon.svg?raw';
import play from './lucide/play.svg?raw';
import rotateCcw from './lucide/rotate-ccw.svg?raw';
import save from './lucide/save.svg?raw';
import search from './lucide/search.svg?raw';
import settings from './lucide/settings.svg?raw';
import share2 from './lucide/share-2.svg?raw';
import skipForward from './lucide/skip-forward.svg?raw';
import sun from './lucide/sun.svg?raw';
import terminal from './lucide/terminal.svg?raw';
import typeIcon from './lucide/type.svg?raw';
import x from './lucide/x.svg?raw';

export type IconName =
	| 'arrow-left'
	| 'arrow-right'
	| 'arrow-up-right'
	| 'ban'
	| 'book'
	| 'book-open'
	| 'check'
	| 'chevron-left'
	| 'chevron-right'
	| 'circle-check'
	| 'circle-help'
	| 'eye'
	| 'eye-off'
	| 'github'
	| 'graduation-cap'
	| 'house'
	| 'layers'
	| 'library'
	| 'lightbulb'
	| 'list'
	| 'loader-circle'
	| 'map'
	| 'menu'
	| 'monitor'
	| 'moon'
	| 'play'
	| 'rotate-ccw'
	| 'save'
	| 'search'
	| 'settings'
	| 'share-2'
	| 'skip-forward'
	| 'sun'
	| 'terminal'
	| 'type'
	| 'x';

export const icons: Record<IconName, string> = {
	'arrow-left': arrowLeft,
	'arrow-right': arrowRight,
	'arrow-up-right': arrowUpRight,
	ban,
	book,
	'book-open': bookOpen,
	check,
	'chevron-left': chevronLeft,
	'chevron-right': chevronRight,
	'circle-check': circleCheck,
	'circle-help': circleHelp,
	eye,
	'eye-off': eyeOff,
	github,
	'graduation-cap': graduationCap,
	house,
	layers,
	library,
	lightbulb,
	list,
	'loader-circle': loaderCircle,
	map,
	menu,
	monitor,
	moon,
	play,
	'rotate-ccw': rotateCcw,
	save,
	search,
	settings,
	'share-2': share2,
	'skip-forward': skipForward,
	sun,
	terminal,
	type: typeIcon,
	x
};
