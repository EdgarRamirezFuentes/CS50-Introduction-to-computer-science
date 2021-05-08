#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
int check_cycle(int loser, int winner);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    //
    for (int i = 0; i < candidate_count; i++)
    {
        // The name given name matches the current candidate's name
        if (!strcmp(name, candidates[i]))
        {
            // Store the index of the voted candidate in the candidates array
            ranks[rank] = i;
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Check the preference of each candidate over the others
    for (int i = 0; i < candidate_count; i++)
    {
        int preferred_candidate = ranks[i];
        for (int j = i + 1; j < candidate_count; j++)
        {
            int unpreferred_candidate = ranks[j];
            // Add up by 1 the preference of the ith candidate over the jth candidate
            preferences[preferred_candidate][unpreferred_candidate]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Compare the ith candidate to the jth candidate to
    // check who is the winner and the loser
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // Store the preference of the ith candidate over the jth candidate
            int preference1 = preferences[i][j];
            // Store the preference of the jth candidate over the ith candidate
            int preference2 = preferences[j][i];
            if (preference1 == preference2)
            {
                continue;
            }
            else if (preference1 > preference2)
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
            }
            else if (preference2 > preference1)
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
            }
            // Increase the current number of pairs
            pair_count++;
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int max_index = 0, winner1, winner2;
    // Use selection sort to sort the pairs in order by decreasing strength of victory
    for (int i = 0; i < pair_count; i++)
    {
        max_index = i;
        // Look for any greater pair in front of the ith pair
        for (int j = i + 1; j < pair_count; j++)
        {
            winner1 = preferences[pairs[max_index].winner][pairs[max_index].loser];
            winner2 = preferences[pairs[j].winner][pairs[j].loser];
            // Check if the greatest preference until now changes
            if (winner2 > winner1)
            {
                max_index = j;
            }
        }

        /*
            * Switch the ith pair with the jth pair, which is greater than the ith pair
        */
        if (max_index != i)
        {
            pair aux_pair = pairs[i];
            pairs[i] = pairs[max_index];
            pairs[max_index] = aux_pair;
        }
    }
    return;
}

int check_cycle(int loser, int winner)
{
    // The winner returned to itself
    if (loser == winner)
    {
        return 1;
    }

    // Check the possible paths
    for (int i = 0; i < candidate_count; i++)
    {
        // Check the path if the loser of the current pair defeated another candidate
        if (locked[loser][i] && check_cycle(i, winner))
        {
            return true;
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    int winner, loser;
    // Lock the possible pairs
    for (int i = 0; i < pair_count; i++)
    {
        winner = pairs[i].winner;
        loser = pairs[i].loser;
        // Check if this pair get a cycle
        if (!check_cycle(loser, winner))
        {
            locked[winner][loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        int victories = 0;

        // Check if there is a candidate that won to our ith candidate
        for (int j = 0; j < candidate_count; j++)
        {
            // The ith candidate won over the jth candidate
            if (!locked[j][i])
            {
                // Add up by 1 the number of candidates that did not win to the ith candidate
                victories++;
                if (victories == candidate_count)
                {
                    printf("%s\n", candidates[i]);
                }
            }
        }
    }
    return;
}

