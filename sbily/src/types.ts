import type { dialog } from "./components/dialog";
import type { closeToast, toast } from "./components/toast";
import type { copy } from "./utils/copy";

declare global {
  interface Window extends WindowWithCustomProps {}
}

export interface WindowWithCustomProps {
  copy: typeof copy;
  toast: typeof toast;
  closeToast: typeof closeToast;
  dialog: typeof dialog;
}

export type EventHandler<T> = (event: T) => void;
