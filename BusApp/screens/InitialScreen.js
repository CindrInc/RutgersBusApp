import * as WebBrowser from 'expo-web-browser';
import Colors from '../constants/Colors'
import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

function InitialScreen() {
    return (
        <View style={styles.container}>
            <View style={styles.headerContainer}>
                <Text style={styles.headerText}>Welcome!</Text>
            </View>
            <View>
                <Image source={require('../assets/images/rutgers.png')} style={styles.rutgersImage}/>
                <Text style={styles.imageSubtitle}>Bus Scheduler</Text>
            </View>
            <TouchableOpacity onPress={this.onGetStarted} style={styles.getStartedButton}>
                <Text style={styles.getStartedButtonText}>Get Started</Text>
            </TouchableOpacity>
        </View>
    )
}

InitialScreen.prototype.onGetStarted = function() {
    console.log("Hello, World!");
}

export default InitialScreen;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Colors.scarlet,
        display: 'flex',
        alignItems: 'center',
    },
    headerContainer: {
        marginBottom: 40
    },
    headerText: {
        marginTop: 50,
        fontWeight: 'bold',
        fontSize: 48,
        color: 'white'
    },
    rutgersImage: {
        width: 304 * 0.7,
        height: 270 * 0.7,
        marginBottom: 10
    },
    imageSubtitle: {
        textAlign: 'center',
        color: 'white',
        fontSize: 24
    },
    getStartedButton: {
        marginTop: 100,
        borderWidth: 3,
        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 10,
        padding: 10
    },
    getStartedButtonText: {
        color: 'white',
        fontSize: 36
    }
});