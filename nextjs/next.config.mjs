/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    async redirects() {
      return [
          {
            source: '/docs',
            destination: '/docs/index.html',
            permanent: true,
          },
          {
            source: '/docs',
            destination: '/docs/index.html',
            permanent: true,
          },
          {
            source: '/docs/api',
            destination: '/docs/api/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/core',
            destination: '/docs/api/core/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/get_started',
            destination: '/docs/api/get_started/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/heat',
            destination: '/docs/api/heat/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/ml',
            destination: '/docs/api/ml/ml/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/llm/yosemite.ml.llm',
            destination: '/docs/api/ml/llm/yosemite.ml.llm/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/data/yosemite.ml.data.database',
            destination: '/docs/api/ml/data/yosemite.ml.data.database/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/data/yosemite.ml.data.yosemite',
            destination: '/docs/api/ml/data/yosemite.ml.data.yosemite/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/data/yosemite.ml.data.vector_database',
            destination: '/docs/api/ml/data/yosemite.ml.data.vector_database/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/transformers/ce',
            destination: '/docs/api/ml/transformers/ce/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/transformers/loss',
            destination: '/docs/api/ml/transformers/loss/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/transformers/semsearch',
            destination: '/docs/api/ml/transformers/semsearch/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/transformers/sentsim',
            destination: '/docs/api/ml/transformers/sentsim/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/transformers/transformer',
            destination: '/docs/api/ml/transformers/transformer/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/yosemite.ml.transformers',
            destination: '/docs/api/ml/yosemite.ml.transformers/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/ml/yosemite.ml.text',
            destination: '/docs/api/ml/yosemite.ml.text/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/core',
            destination: '/docs/api/core/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/tools/yosemite.tools.input',
            destination: '/docs/api/tools/yosemite.tools.input/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/tools/yosemite.tools.text',
            destination: '/docs/api/tools/yosemite.tools.text/index.html',
            permanent: true,
          },
          {
            source: '/docs/api/tools/yosemite.tools.load',
            destination: '/docs/api/tools/yosemite.tools.load/index.html',
            permanent: true,
          },
      ];
    },
  };
  
export default nextConfig;