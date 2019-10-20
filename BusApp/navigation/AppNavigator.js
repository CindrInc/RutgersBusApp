import React from 'react';
import { createAppContainer, createSwitchNavigator } from 'react-navigation';

import MainTabNavigator from './MainTabNavigator';
import InitialScreen from '../screens/InitialScreen';

export default createAppContainer(
  createSwitchNavigator(
    {
      Initial: InitialScreen,
      Main: MainTabNavigator,
    }
  )
);
