import { useEffect } from 'react';
import { useRouter } from 'next/router';

const Docs = () => {
  const router = useRouter();

  useEffect(() => {
    router.push('/html/index.html');
  }, []);

  return null;
};

export default Docs;