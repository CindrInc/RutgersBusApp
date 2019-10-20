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

export default class LinksScreen extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      loading: true
    }
  }

  componentDidMount() {
    this.getLocationAsync()
  }

  getLocationAsync = async () => {
    try {
      let { status } = await Permissions.askAsync(Permissions.LOCATION);
      if (status !== 'granted') {
        this.setState({
          errorMessage: 'Permission to access location was denied',
        });
      }

      let location = await Location.getCurrentPositionAsync({});
      let url = 'http://172.31.81.151:5000/getClosestStop?latitude=' + location.coords.latitude + '&longitude=' + location.coords.longitude;
      let resp = await fetch(url);
      let respJson = await resp.json()
      let stop = respJson.closestStop
      let min = parseInt(respJson.mins)

      url = 'http://172.31.81.151:5000/getBusPrediction?stop=' + stop
      resp = await fetch(url);
      respJson = await resp.json()
      let pred = parseInt(respJson.estimates[0].substring(2,4))

      url = 'http://172.31.81.151:5000/getBus2Bus?stop=' + stop
      resp = await fetch(url);
      respJson = await resp.json()

      this.setState({
        loading: false,
        closestStop: stop,
        mins: min,
        pred: pred,
        busTime: Math.round(respJson.estimate)
      });

      // url = 'http://172.31.81.151:5000/sendText?walk=' + this.state.mins + '&time=' + this.state.pred
      url = 'http://172.31.81.151:5000/sendText?walk=' + this.state.mins + '&time=' + this.state.pred + '&busTime=' + this.state.busTime
      resp = await fetch(url);
    } catch (err) {
      console.log(JSON.stringify(err))
    }
  }

  render() {
    let view;
    if (this.state.loading) {
      view = <ActivityIndicator size="large"/>
    } else {
      view = (
        <View>
          <Text style={styles.closestStopText}>Closest stop is {this.state.closestStop} which is {this.state.mins} mins away.</Text>
          <Text style={styles.closestStopText}>Your next class is at LSH-AUD.</Text>
          <Text style={styles.closestStopText}>The next Weekend 1 bus is arriving in {this.state.pred} mins.</Text>
          {/* <Text style={styles.closestStopText}>The bus ride plus time to walk will take {this.state.mins + this.state.pred + 10} min.</Text> */}
          <Text style={styles.closestStopText}>The bus ride plus time to walk will take {this.state.mins + this.state.pred + this.state.busTime} min.</Text>
        </View>
      )
    }
    return (
      <View style={styles.container}>
        {view}
      </View>
    );
  }
}

LinksScreen.navigationOptions = {
  title: 'Bus Predictions',
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    backgroundColor: '#fff',
  },
  closestStopText: {
    fontSize: 18,
    marginBottom: 5,
    marginLeft: 10
  }
});
