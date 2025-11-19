/**
 * Application methods
 */
import bootstrap from './bootstrap.js';
import destroy from './destroy.js';
import register from './register.js';

/**
 * Plugin server methods
 */
import config from './config/index.js';
import contentTypes from './content-types/index.js';
import controllers from './controllers/index.js';
import middlewares from './middlewares/index.js';
import policies from './policies/index.js';
import routes from './routes/index.js';
import services from './services/index.js';

export default {
  register,
  bootstrap,
  destroy,
  config,
  controllers,
  routes,
  services,
  contentTypes,
  policies,
  middlewares,
};
