#Interview technical problem

---

Assume you are given set of files listing events in people's calendars.
File with such a content:
2022-06-01 12:00:00 - 2022-06-01 12:59:59
2022-06-01 15:20:00 - 2022-06-01 15:49:59
means that a person on 2022-06-01 is busy for one hour at 12:00 and busy for half an hour at 15:20.
Additionally, if a line in that file consists only of a date (like "2022-07-01") then it means a person is busy whole
day. Separate file for each person.
Prepare a script that will print out the soonest date in the future when at least desired amount of people are
available for given amount of time. Script should accept a named parameter --duration-in-minutes which
defines for how many minutes people should be available. Minumum number of people that must be available
should be defined by --minimum-people argument. Script should read people's calendars from \*.txt files in the
directory provided as an --calendars string.

---

Example
Assuming it's 2022-07-01 09:00:00 now and:

- file /in/alex.txt consists of:
  2022-07-02 13:15:00 - 2022-06-01 13:59:59
- file /in/brian.txt consists of:
  2022-07-01
  2022-07-02 00:00:00 - 2022-07-02 12:59:59

---

Calling the script:
python3 find-available-slot.py --calendars /in --duration-in-minutes 30 --minumum-people 2
should print out:
2022-07-02 14:00:00

---

###Sample calendar of 5 people:

![calendar](/terminal.png)

---

### How to run the script

- clone the reposiroty\
  `git clone https://github.com/KostkaMateusz/zadanie2.git`

- run command\
  `python3 find-available-slot.py --calendars /in --duration-in-minutes 30 --minumum-people 2`

- in order to run the tests\
   "yet to come"
