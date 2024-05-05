

import * as React from 'react';
import HeaderLayout from './header';

export interface IAppProps {
}

export function Home (props: IAppProps) {
  return (
    <div>
      <HeaderLayout/>
    </div>
  );
}

export default Home;
