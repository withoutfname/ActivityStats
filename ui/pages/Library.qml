import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Component.onCompleted: {
        console.log("Fetching games...")
        libraryController.fetchGames()
        console.log("Games fetched:", JSON.stringify(libraryController.gamesList))
    }

    ScrollView {
        id: scrollView
        anchors.fill: parent
        clip: true
        ScrollBar.vertical.policy: ScrollBar.AsNeeded
        ScrollBar.horizontal.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: scrollView.width
            spacing: 30

            Label {
                text: "Game Library"
                font.pixelSize: 28
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 10
            }

            Loader {
                id: noDataLoader
                active: libraryController.gamesList.length === 0
                sourceComponent: Component {
                    Label {
                        text: "No games found in the library."
                        font.pixelSize: 20
                        color: "gray"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
            }

            GridView {
                id: gameGrid
                Layout.fillWidth: true
                Layout.preferredHeight: contentHeight
                Layout.leftMargin: 30
                Layout.rightMargin: 30
                cellWidth: (parent.width - Layout.leftMargin - Layout.rightMargin) / 5 - 20
                cellHeight: 360
                model: libraryController.gamesList
                visible: libraryController.gamesList.length > 0

                property int itemSpacing: 20

                delegate: Item {
                    id: cellItem
                    width: gameGrid.cellWidth - gameGrid.itemSpacing
                    height: gameGrid.cellHeight

                    Rectangle {
                        id: card
                        width: parent.width
                        height: 340
                        color: "white"
                        border.color: "gray"
                        border.width: 1
                        radius: 5
                        clip: true

                        Column {
                            id: contentColumn
                            anchors.top: parent.top
                            anchors.topMargin: 10
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 5
                            width: parent.width - 20

                            Image {
                                id: gameImage
                                source: Qt.resolvedUrl(modelData.icon_path).toString()
                                width: 140
                                height: 140
                                fillMode: Image.PreserveAspectFit
                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Text {
                                text: modelData.name || "Unnamed Game"
                                font.pixelSize: 14
                                horizontalAlignment: Text.AlignHCenter
                                width: parent.width
                                wrapMode: Text.WordWrap
                            }

                            Text {
                                text: "Hours: " + (modelData.total_hours || 0).toFixed(1)
                                font.pixelSize: 12
                                color: "gray"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        Column {
                            id: hoverInfo
                            anchors.top: contentColumn.bottom
                            anchors.topMargin: 10
                            anchors.horizontalCenter: parent.horizontalCenter
                            spacing: 5
                            width: parent.width - 20
                            visible: false

                            Text {
                                text: "Sessions: " + (modelData.session_count || 0)
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "First Played: " + (modelData.first_played ? Qt.formatDate(new Date(modelData.first_played), "dd-MM-yyyy") : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Last Played: " + (modelData.last_played ? Qt.formatDate(new Date(modelData.last_played), "dd-MM-yyyy") : "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Genre: " + (modelData.genre || "Unknown")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                text: "Year: " + (modelData.year || "N/A")
                                font.pixelSize: 12
                                color: "black"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }



                        // Кнопки в правом нижнем углу
                        RowLayout {
                            id: buttonRow
                            anchors.right: parent.right
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 10
                            anchors.bottomMargin: 10
                            spacing: 5
                            visible: true  // Скрыты по умолчанию

                            Button {
                                id: autoButton
                                implicitWidth: 40
                                implicitHeight: 40
                                background: Rectangle {
                                    color: "transparent"
                                    radius: 5
                                }
                                Image {
                                    source: Qt.resolvedUrl("../../resources/images/auto_parse_icon.png").toString()
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    fillMode: Image.PreserveAspectFit
                                }
                                onClicked: {
                                    console.log("Auto parse clicked for", modelData.name)
                                    // Здесь код для авто парсинга
                                }
                            }

                            Button {
                                id: manualButton
                                implicitWidth: 40
                                implicitHeight: 40
                                background: Rectangle {
                                    color: "transparent"
                                    radius: 5
                                }
                                Image {
                                    source: Qt.resolvedUrl("../../resources/images/manual_icon.png").toString()
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    fillMode: Image.PreserveAspectFit
                                }
                                onClicked: {
                                    console.log("Manual parse clicked for", modelData.name)
                                    editDialog.open()
                                }
                            }
                        }

                        MouseArea {
                            anchors.fill: hoverInfo
                            hoverEnabled: true
                            onEntered: {
                                card.color = "#f0f0f0"
                                hoverInfo.visible = true
                                //buttonRow.visible = true
                            }
                            onExited: {
                                card.color = "white"
                                hoverInfo.visible = false
                                //buttonRow.visible = false
                            }
                        }
                    }
                }
            }
        }
    }

    // Простой диалог внутри Library.qml
    Dialog {
        id: editDialog
        title: "Edit Game Metadata"
        standardButtons: Dialog.Close  // Кнопка закрытия

        width: 200
        height: 100

        Label {
            anchors.centerIn: parent
            text: "Привет"
            font.pixelSize: 16
        }
    }
}