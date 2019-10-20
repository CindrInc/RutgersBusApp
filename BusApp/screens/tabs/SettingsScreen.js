import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  AsyncStorage,
  ActivityIndicator
} from 'react-native';
import Constants from 'expo-constants';
import * as Location from 'expo-location';
import * as Permissions from 'expo-permissions';

export default class SettingsScreen extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <ScrollView>
          <Text style={styles.settingsText}>Settings</Text>
          <View style={styles.extraTime}>
            <Text style={styles.descrt}>Add this time to the prediction so you're there early</Text>
            <Text style={styles.extra}>5 min</Text>
          </View>
        </ScrollView>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  conatiner: {
    flex: 1
  },
  settingsText: {
    fontSize: 36,
    fontWeight: 'bold',
    marginTop: 40,
    marginLeft: 10,
    marginBottom: 10
  },
  extraTime: {
    display: 'flex',
    flexDirection: 'row',
    backgroundColor: '#efefef',
    padding: 10
  },
  descrt: {
    fontSize: 18,
    width: 250,
    textAlign: "right",
    paddingRight: 10,
    borderRightWidth: 1,
    borderColor: 'black'
  },
  extra: {
    fontSize: 18,
    paddingLeft: 15
  }
});

SettingsScreen.navigationOptions = {
  header: null
};
