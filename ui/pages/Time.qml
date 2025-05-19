import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    Component.onCompleted: {
        rangeSlider.first.value = 0
        rangeSlider.second.value = 120
        timeController.setIntervalRange(0, 120)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        Label {
            text: "Time Stats"
            font.pixelSize: 28
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        RangeSlider {
            id: rangeSlider
            from: 0
            to: timeController.maxIntervalDays
            first.value: 0
            second.value: 25
            stepSize: 1
            Layout.fillWidth: true
            snapMode: RangeSlider.SnapAlways
            first.onMoved: timeController.setIntervalRange(Math.floor(first.value), Math.floor(second.value))
            second.onMoved: timeController.setIntervalRange(Math.floor(first.value), Math.floor(second.value))
        }

        Label {
            text: {
                var start = Qt.formatDate(new Date(timeController.startDate), "dd-MM-yyyy");
                var end = Qt.formatDate(new Date(timeController.endDate), "dd-MM-yyyy");
                return "Period: " + start + " to " + end
            }
            font.pixelSize: 18
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Playtime: " + timeController.fullTotalPlaytime + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Average Session Time: " + timeController.avgSessionTime + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Average Day Playtime: " + timeController.avgDayPlaytime.toFixed(1) + " hours"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Total Sessions: " + timeController.simpSessionCount
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Session Duration: " + timeController.maxSessionDuration[0].toFixed(1) + " hours (Date: " + timeController.maxSessionDuration[2] + ", Game: " + timeController.maxSessionDuration[1] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Daily Game Session: " + timeController.maxDailyGameSession[0].toFixed(1) + " hours (Date: " + timeController.maxDailyGameSession[1] + ", Game: " + timeController.maxDailyGameSession[2] + ", Sessions: " + timeController.maxDailyGameSession[3] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Max Daily Total Duration: " + timeController.maxDailyTotalDuration[0].toFixed(1) + " hours (Date: " + timeController.maxDailyTotalDuration[1] + ", Games: " + timeController.maxDailyTotalDuration[2] + ")"
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "Playtime by Day of Week:"
            font.pixelSize: 20
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            spacing: 20
            Layout.alignment: Qt.AlignHCenter

            Canvas {
                id: histogramCanvas
                width: 600
                height: 300
                Layout.alignment: Qt.AlignLeft

                property var playtime: timeController.playtimeByDayOfWeek
                property var dayNames: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

                onPlaytimeChanged: requestPaint()

                onPaint: {
                    var ctx = getContext("2d");
                    ctx.reset();

                    // Определяем максимальное значение для масштабирования
                    var maxValue = Math.max(...playtime);
                    if (maxValue === 0) maxValue = 1; // Избегаем деления на ноль

                    // Параметры гистограммы
                    var barWidth = width / 8; // 7 столбиков + промежутки
                    var margin = barWidth; // Увеличиваем отступ слева
                    var heightScale = (height - 30) / maxValue; // Отступ снизу для подписей

                    // Ось X (дни недели)
                    ctx.beginPath();
                    ctx.moveTo(margin, height - 20);
                    ctx.lineTo(width - margin / 2, height - 20);
                    ctx.strokeStyle = "#000000";
                    ctx.stroke();

                    // Подписи по оси X
                    ctx.font = "14px sans-serif";
                    ctx.fillStyle = "#000000";
                    ctx.textAlign = "center";
                    for (var i = 0; i < 7; i++) {
                        var x = margin + (i + 0.5) * barWidth;
                        ctx.fillText(dayNames[i], x, height - 5);
                    }

                    // Ось Y (часы)
                    ctx.beginPath();
                    ctx.moveTo(margin, 10);
                    ctx.lineTo(margin, height - 20);
                    ctx.stroke();

                    // Подписи по оси Y (пример: 0, maxValue)
                    ctx.font = "12px sans-serif";
                    ctx.textAlign = "right";
                    ctx.fillText(maxValue.toFixed(1) + "h", margin - 10, 15);
                    ctx.fillText("0h", margin - 10, height - 20);

                    // Рисуем столбики
                    for (var j = 0; j < 7; j++) {
                        // Сдвигаем индексы: Пн (j=0) -> playtime[1], ..., Вс (j=6) -> playtime[0]
                        var playtimeIndex = (j + 1) % 7;
                        var barHeight = playtime[playtimeIndex] * heightScale;
                        var xPos = margin + j * barWidth;
                        ctx.fillStyle = "#4CAF50"; // Цвет столбиков
                        ctx.fillRect(xPos, height - 20 - barHeight, barWidth - 5, barHeight);
                    }
                }
            }

            ColumnLayout {
                spacing: 5
                Layout.alignment: Qt.AlignTop

                Repeater {
                    model: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
                    Label {
                        text: modelData + ": " + timeController.playtimeByDayOfWeek[(index + 1) % 7].toFixed(1) + " hours"
                        font.pixelSize: 18
                        Layout.alignment: Qt.AlignLeft
                    }
                }
            }
        }

        Connections {
            target: timeController
            function onIntervalChanged() {
                console.log("Interval changed, updating UI")
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }
}