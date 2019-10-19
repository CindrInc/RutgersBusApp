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

export default function InitialScreen() {
    return (
        <View style={styles.container}>
            <View>
                <Text style={styles.headerText}>Hello, World!</Text>
            </View>
            <Image source={require('../assets/images/rutgers.png')}/>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: Colors.scarlet
    },
    headerText: {
        marginTop: 50,
        textAlign: 'center',
        fontWeight: 'bold',
        color: 'white',
        fontSize: 48
    }
});