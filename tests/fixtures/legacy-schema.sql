CREATE TABLE `decisions` (
	`id` text PRIMARY KEY NOT NULL,
	`cycle` integer NOT NULL,
	`at` text NOT NULL,
	`record` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `decisions_cycle_idx` ON `decisions` (`cycle`);--> statement-breakpoint
CREATE TABLE `organisms` (
	`id` text PRIMARY KEY NOT NULL,
	`state` text NOT NULL,
	`revision` integer DEFAULT 0 NOT NULL,
	`lease` text,
	`lease_until` integer DEFAULT 0 NOT NULL
);
