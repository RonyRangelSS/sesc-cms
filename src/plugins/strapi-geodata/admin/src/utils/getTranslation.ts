import { PLUGIN_ID } from '../pluginId.js';

const getTranslation = (id: string) => `${PLUGIN_ID}.${id}`;

export { getTranslation };
