import * as WebBrowser from 'expo-web-browser';
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
import NavigationEvents from 'react-navigation';
import Colors from '../../../constants/Colors';

export default class HomeScreen extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      // locationLoading: true,
      scheduleLoading: true,
      // location: {
      //   latitude: 0,
      //   longitude: 0
      // },
      schedule: []
    }
    this.focusListener = this.props.navigation.addListener('didFocus', () => {
      this.getScheduleAsync()
    });
  }

  componentDidMount() {
    this.getScheduleAsync()
  }

  componentWillUnmount() {
    this.focusListener.remove()
  }

  getScheduleAsync = async() => {
    try {
      let schedule = await AsyncStorage.getItem('schedule')
      if (schedule === null) {
        schedule = '[]'
      }
      this.scheduleLoaded(schedule)
    } catch (e) {
      this.scheduleLoaded('[]')
    }
  }

  scheduleLoaded(value) {
    let sched = JSON.parse(value)
    this.setState({
      scheduleLoading: false,
      schedule: sched
    })
  }

  render() {
    if (/*this.state.locationLoading || */this.state.scheduleLoading) {
      return (
        <View style={styles.container}>
          <ActivityIndicator style={styles.spinner} size='large'/>
        </View>
      )
    }

    let scheduleView;
    if (this.state.schedule.length != 0) {

      let classViews = [];
      for (let i = 0; i < 4; i++) {
        let currClass = this.state.schedule[i];
        classViews.push(
          <Text key={i} style={styles.classView}>- {currClass.name} at {currClass.build} on {currClass.day}'s from {currClass.start} to {currClass.end}</Text>
        );
      }

      scheduleView = (
        <View style={styles.bloo}>
          <Text style={styles.scheduleTextAvail}>Your Class Schedule</Text>
          {classViews}
          <TouchableOpacity style={styles.enterScheduleBtn} onPress={this.onEnterSchedule}>
            <Text style={styles.enterScheduleBtnText}>Edit</Text>
          </TouchableOpacity>
        </View>
      )
    } else {
      scheduleView = (
        <View style={styles.scheduleTextEmptyContainer}>
          <Text style={styles.scheduleTextEmpty}>You have an empty schedule! Enter your information.</Text>
          <TouchableOpacity style={styles.enterScheduleBtn} onPress={this.onEnterSchedule}>
            <Text style={styles.enterScheduleBtnText}>Go</Text>
          </TouchableOpacity>
        </View>
      )
    }

    return (
      <View style={styles.container}>
        {scheduleView}
      </View>
    )
  }

  onEnterSchedule = () => {
    this.props.navigation.push('Input')
  }
}

HomeScreen.navigationOptions = {
  header: null,
};

// function handleLearnMorePress() {
//   WebBrowser.openBrowserAsync(
//     'https://docs.expo.io/versions/latest/workflow/development-mode/'
//   );
// }

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  spinner: {
    marginTop: 40
  },
  scheduleTextAvail: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 10,
  },
  classView: {
    fontSize: 18,
    marginBottom: 5
  },
  bloo: {
    display: 'flex',
    alignItems: 'center'
  },
  scheduleTextEmptyContainer: {
    display: 'flex',
    alignItems: 'center'
  },
  scheduleTextEmpty: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 10
  },
  enterScheduleBtn: {
    borderWidth: 2,
    borderStyle: 'solid',
    borderColor: Colors.scarlet,
    borderRadius: 10,
    padding: 6,
    width: 50
  },
  enterScheduleBtnText: {
    fontWeight: 'bold',
    color: Colors.scarlet,
    textAlign: 'center'
  }
});