import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "ActivityStats"

    // Store absolute paths for tabs
    property var tabSources: [
        Qt.resolvedUrl("../ui/pages/Dashboard.qml").toString(),
        "", // Games (WIP)
        "", // Time (WIP)
        "", // Records (WIP)
        ""  // Library (WIP)
    ]

    header: TabBar {
        id: tabBar
        width: parent.width

        TabButton { text: "Dashboard" }
        TabButton { text: "Games" }
        TabButton { text: "Time" }
        TabButton { text: "Records" }
        TabButton { text: "Library" }
    }

    Loader {
        id: pageLoader
        anchors.fill: parent
        source: tabSources[tabBar.currentIndex]
    }

    Label {
        anchors.centerIn: parent
        text: "Page Not Implemented"
        font.pixelSize: 20
        visible: pageLoader.status !== Loader.Ready
    }
}