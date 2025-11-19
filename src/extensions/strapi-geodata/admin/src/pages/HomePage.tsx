import { Main } from '@strapi/design-system';
import { useIntl } from 'react-intl';

import { Typography, BaseLink } from '@strapi/design-system';
import { Box } from '@strapi/design-system';

import PluginIcon from './../components/PluginIcon';

const HomePage = () => {
  const { formatMessage } = useIntl();

  return (
    <Main>
      <Box
        style={{
          padding: '2rem',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        }}
      >
        <Box>
          <Typography variant="alpha" style={{ fontWeight: 'bold', marginBottom: '1rem' }}>
          <PluginIcon style={{width: "3rem", height:"3rem"}} />
          {' '}Welcome to GeoData
          </Typography>
        </Box>
        <Box>
          <Typography
            variant="beta"
            style={{ fontWeight: '600', marginBottom: '0.5rem', color: '#e65100' }}
          >
            Important Note:
          </Typography>
        </Box>
        <Box>
          <Typography variant="gamma" style={{ lineHeight: '1.6' }}>
            Only one GeoJSON field is allowed per content type. To store latitude, longitude, and
            geohash separately for queries, create three fields: <strong>lat</strong> (float),{' '}
            <strong>lng</strong> (float), and <strong>geohash</strong> (string). The plugin
            automatically updates the lat/lng fields and the geohash field whenever any of these
            fields are modified. For dynamic creation, write the GeoJSON field in the{' '}
            <code>{`{lat, lng}`}</code> format, and the related fields will be populated
            automatically.
          </Typography>
          <Box style={{ marginTop: '2rem', padding: '1rem', borderTop: '1px solid #ddd' }}></Box>
          <Typography variant="gamma" style={{ lineHeight: '1.6' }}>
            To set a field as a float, first create a numeric input, then modify the schema to define it as a float.
          </Typography>
        </Box>
        <Box style={{ marginTop: '2rem', padding: '1rem', borderTop: '1px solid #ddd' }}>
          <Typography variant="beta" style={{ fontWeight: '600', marginBottom: '0.5rem' }}>
            Contact the Author:{' '}
          </Typography>
          <Typography variant="gamma" style={{ lineHeight: '1.6' }}>
            For inquiries, please contact the author at:{' '}
            <Typography style={{ fontWeight: "bold" }}>info@red-made.com</Typography> or visit the{' '}
            <BaseLink style={{ fontWeight: "bold" }} href="https://github.com/red-made/strapi-geodata" target="_blank" rel="noopener noreferrer">
              GitHub repository @github.com/red-made/strapi-geodata
            </BaseLink>
            .
          </Typography>
        </Box>
      </Box>
    </Main>
  );
};

export { HomePage };
