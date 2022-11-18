# Homework 6
- [Homework 6](#homework-6)
  - [Exercise 1: [attack] Just In Time](#exercise-1-attack-just-in-time)
  **Never use your actual GASPAR password on COM-402 exercises (if the login form is not Tequila).**

## Exercise 1: [attack] Just In Time

**Please, try to do this exercise without looking into the files that are in the docker as it is simulating an external server to which you can only send POST requests**.



In this exercise, you’re being asked to guess credentials on a website.

You will run the website locally by doing:

`docker run --rm -it -p 8080:8080 --name hw6ex1 com402/hw6ex1`

Then, to login, you must send a POST request with a JSON body looking like:

   {"token": yourguessedtoken }

to

   http://0.0.0.0:8080/hw6/ex1

<sub>Note, remember to use the `JSON` body, and not the `form` body (we are not submitting a form). The Python syntax is slightly different from what you learned last week.</sub>

Don’t try to brute force the token. There are much faster ways to guess the correct token.

For example, the developer here used a modified function to compare strings that express some very specific timing behavior for each valid character in the submitted token…

The response code is 500 when the token is invalid and 200 when the token is valid. Look at the body of the response, you can get some useful information too.

This exercise will require some patience and trial-and-error, as time in networks is never 100% accurate. In order to be precise, you should calibrate your measurements first, before trying to do any guessing on the token. 

### Calibration

When using a timing-sensitive string comparison, correctly guessing one extra character of the password will cause a bit more computation on the server since the comparison will continue for one extra iteration. You can test this by trying two-character passwords, with the first character ranging from [`a`, `z`] or [`0`, `9`]. For one of the guesses, you will match the first character of the password and proceed to check the second character, taking slightly longer. 

For each of the 36 guesses, time a large number of requests and plot the average for each. You should be able to identify the correct character clearly by a spike in the time taken. Note that we have purposefully amplified the delta in timing in order to simplify your life. 

### Guessing

Follow this algorithm, starting with n = 2.

1. Create a string of length `n` where the first `n-2` characters are known. Create the set of guesses by varying the `n-1`th character within the set of possible characters. Set the `n`th character to whatever. This is merely to ensure that some processing happens after the correct `n-1`th comparison succeeds.
2. For each guess, calculate the mean request time over a large number of requests. 
3. Identify the correct `n-1`th character based on the timing channel
4. Increment `n` by 1 and return to step 1.


> We recommend taking a large number of measurements. For different levels of noise in the channel, how does the required number of measurements change in order to get the same confidence for a guess?

### Verification

Get a 200 response code. 
To verify that you retrieved the correct token you can also check the file inside the docker container:

`/root/solutions/solution.txt`