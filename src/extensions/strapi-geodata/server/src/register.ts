import type { Core } from '@strapi/strapi';

const register = ({ strapi }: { strapi: Core.Strapi }) => {
  // register phase
  strapi.customFields.register({
    name: "geojson",
    plugin: "geodata",
    type: "json",
    inputSize: {
      // optional
      default: 12,
      isResizable: true,
    },
  });

};

export default register;
