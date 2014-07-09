// Reference: http://main.edu.pl/en/archive/oi/13/kra

#include <algorithm>
#include <iostream>
#include <deque>
#include <sstream>
#include <vector>

#include <gtest/gtest.h>

using namespace std;

void solve(istream & in, ostream & out) {
    unsigned numberOfCylinders, numberOfDisks;
    in >> numberOfCylinders >> numberOfDisks;

    vector<unsigned> cylinders;
    cylinders.reserve(numberOfCylinders);

    unsigned diameter;

    { /// Get cylinders.
        unsigned minDiameter = numeric_limits<unsigned>::max();

        for (unsigned i = 0; i < numberOfCylinders; ++i) {
            in >> diameter;
            minDiameter = min(diameter, minDiameter);
            cylinders.push_back(minDiameter);
        }
    }

    deque<unsigned> disks;

    { /// Get disks.
        for (unsigned i = 0; i < numberOfDisks; ++i) {
            in >> diameter;
            disks.push_back(diameter);
        }
    }

    unsigned filledOrBlockedCylinders = 0;

    { /// Solve.
        while (!disks.empty()) {
            diameter = disks.front();
            disks.pop_front();

            while (!cylinders.empty() && diameter > cylinders.back()) {
                filledOrBlockedCylinders++;
                cylinders.pop_back();
            }

            if (!cylinders.empty()) {
                filledOrBlockedCylinders++;
                cylinders.pop_back();
            }
        }
    }

    unsigned depth = numberOfCylinders - filledOrBlockedCylinders;
    out <<  ((depth != 0) ? (depth + 1) : 0) << endl;
}

TEST(Kra13, SampleFromWebPage) {
    istringstream in(
        "7 3\n"
        "5 6 4 3 6 2 3\n"
        "3 2 5\n");
    stringstream out;
    solve(in, out);

    ASSERT_EQ("2\n", out.str());
}

TEST(Kra13, NoDisksCanFitIn) {
    istringstream in(
        "10 10\n"
        "10 9 8 7 6 5 4 3 2 1\n"
        "11 10 9 8 7 6 5 4 3 2\n");
    stringstream out;
    solve(in, out);

    ASSERT_EQ("0\n", out.str());
}

TEST(Kra13, LastButOneDiskCanNotFit) {
    istringstream in(
        "10 10\n"
        "10 9 8 7 6 5 4 3 2 1\n"
        "1 2 3 4 5 6 7 8 11 9\n");
    stringstream out;
    solve(in, out);

    ASSERT_EQ("0\n", out.str());
}

TEST(Kra13, LastDiskCanNotFit) {
    istringstream in(
        "10 10\n"
        "10 9 8 7 6 5 4 3 2 1\n"
        "1 2 3 4 5 6 7 8 9 11\n");
    stringstream out;
    solve(in, out);

    ASSERT_EQ("0\n", out.str());
}

TEST(Kra13, AllDisksFitCylinders) {
    istringstream in(
        "10 10\n"
        "10 9 8 7 6 5 4 3 2 1\n"
        "1 2 3 4 5 6 7 8 9 10\n");
    stringstream out;
    solve(in, out);

    ASSERT_EQ("0\n", out.str());
}

// TODO: Test big sets of data.

int main(int ac, char ** av) {
#ifdef BUILD_FOR_TARGET
    cin.sync_with_stdio(false);
    solve(cin, cout);
#else
    ::testing::InitGoogleTest(&ac, av);
    return RUN_ALL_TESTS();
#endif
}

