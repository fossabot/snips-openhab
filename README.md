# Snips-OpenHAB

Skill für [Snips.ai](https://snips.ai) zur Ansteuerung von Geräten mit [OpenHAB](https://openhab.org).

## Konfiguration

Folgende secret-Parameter müssen konfiguriert werden:

* openhab_server_url: URL des OpenHAB-Servers (z.B. http://localhost:8080)
* room_of_device_default: Name des Raums, in dem sich das Snips-Gerät mit der Kennzeichnung default befindet

Snips-OpenHAB verwendet [Semantic Tagging](https://community.openhab.org/t/habot-walkthrough-2-n-semantic-tagging-item-resolving/), um die korrekten Items zu finden.

**Wichtig**: Snips-OpenHAB findet nur Items, die Teil einer Gruppe sind, welche als eine Location getaggt ist. Desweiteren muss in der Paper UI unter Preferences die Sprache von OpenHAB auf deutsch eingestellt werden.

## Verwendung

Aktuell sind folgende Befehle implementiert:

* Items vom Typ Switch ein- und ausschalten
* Die Temperatur eines Raums ausgeben
* Items vom Typ Dimmer erhöhen und verringern
* Items vom Typ Player steuern (Play, Pause, Next, Previous)

Bei Anfragen muss stets der Raum genannt werden, in dem sich das Gerät befindet. Es gibt nur die folgenden Ausnahmen:

* Die Anfrage referenziert eindeutig ein Gerät (z.B. Fernseher den einzigen Fernseher). Sagt der Nutzer z.B. Tischlampe und es gibt mehr als ein Item in der Wohnung mit dem Label Tischlampe funktioniert dies nicht.
* Die angesprochenen Geräte befinden sich im aktuellen Raum

Die Trainingsdaten für die einzelnen Intens befinden sich zur Dokumentation im Unterordner `training`.

### Geräte ein- und ausschalten

Items vom Typ `Switch` lassen sich wie folgt ein- und ausschalten:

* Schalte den Fernseher im Wohnzimmer aus
* Schalte das Licht im Schlafzimmer an
* Schalte mir bitte die Hintergrundbeleuchtung aus
* Schalte die Steckdosen in der Wohnung aus

Es ist ebenfalls möglich mehrere Items auf einmal ein- und auszuschalten:

* Schalte die Anlage und den Fernseher ein

Die Items müssen sich dazu im selben Raum befinden.
Die Angabe von mehreren Räumen auf einmal wird aktuell nicht unterstützt.

Beispiel:

```text
Switch Anlage_An_Aus "Anlage" <player> (schlafzimmer) ["Receiver"]
```

### Temperatur

Die Temperatur eines Raums lässt sich wie folgt ausgeben:

* Wie warm ist es im Schlafzimmer?
* Ist es in der Küche Kalt?
* Wie warm ist es hier?

Um die Temperatur eines Raums zu bestimmen sucht Snips-OpenHAB nach
Items vom Typ ```Number``` im gewünschten Raum, die den 
Tag ```Temperature``` und ```Measurement``` besitzen.

Beispiel:

```text
Number Temperature_Bedroom "Temperatur [%.1f °C]" <temperature> (schlafzimmer) ["Temperature", "Measurement"]
```

### Werte erhöhen und verringern

Items vom Typ ```Dimmer``` können mit folgenden Befehlen verändert werden.

* Verringere die Temperatur im Schlafzimmer
* Mache die Musik lauter
* Erhöhe die Helligkeit im Wohnzimmer

Die Items müssen dazu mit ihrer Eigenschaft (z.B. ```Temperature```) und dem Tag ```Setpoint``` getaggt sein.

Beispiel:

```text
Dimmer Anlage_Volume "Lautstärke" <soundvolume> (schlafzimmer) ["SoundVolume", "Setpoint"]
```

### Wiedergabe steuern

Items vom Typ ```Player``` können ebenfalls gesteuert werden:

* Setze die Wiedergabe fort
* Pausiere die Wiedergabe im Wohnzimmer
* Spiele das vorherige Lied
* Wechsle zum nächsten Lied

Beispiel:

```text
Player Wohnzimmer_Control "Fernbedienung" <mediacontrol> (wohnzimmer) ["RemoteControl"]
```

## Synonyme

Durch das Taggen werden automatisch nützliche Synonyme hinzugefügt, über die das Gerät angesprochen werden kann.
Sind diese nicht ausreichend lassen sich noch weitere Synonyme hinzufügen.

Beispiel:

```text
Switch Ventilator "Ventilator" [%.1f °C]" <temperature> (schlafzimmer) { synonyms="Propeller,Windmaschine" }
```

## Multi-Room

Die App ist Multi-Room-fähig. Wird der Raum in einem Befehl weggelassen sucht
Snips-OpenHAB nach Geräten in dem Raum, in dem sich der angesprochene Snips-Satellit befindet.
Dazu wird die ```siteID``` als Raumname verwendet. 
Für das Gerät ```default``` wird als Raumname der Wert des Parameters ```room_of_device_default``` verwendet.
