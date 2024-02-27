# Worlds Worst API

An API containing some of the worst design decisions known to humanity...

![A cute plushie llama looking like a devil](./img/devil-llama.webp)

## Run the API

This API is written in FastAPI, and can be run using the following command:

```bash
cd src
uvicorn main:app --reload
```

You will need to install the dependencies first, by either installing them from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Or by running this inside the provided dev container. In the dev container, the dependencies are already installed.

## All the API worst practices...

This API has all the following worst practices:

- [Documentation as screenshots in Excel](#documentation-as-screenshots-in-excel)
- [GET for all operations](#get-for-all-operations)
- [Terrible naming](#terrible-naming)
- [Not using path parameters](#not-using-path-parameters)
- [Always returning 200](#always-returning-200)
- [Non-atomic updates](#non-atomic-updates)
- [Inconsistent data types](#inconsistent-data-types)

### Documentation as screenshots in Excel

As we all know - the best documentation is not an [OpenAPI](https://www.openapis.org) spec, or fancy generated docs using the spec, but screenshots inside Excel. After all, attaching screenshots to Excel spreadsheets is even a practice internal teams at Microsoft use today (ask me how I know...).

The documentation is included in this repo in the [`Worlds Worst API documentation.xlsx`](./Worlds%20Worst%20API%20documentation.xlsx) Excel spreadsheet.

> Don't tell our users, but you can also access the OpenAPI spec once this app is running at [`localhost:8000/openapi.json`](http://localhost:8000/openapi.json), and generated docs at [`localhost:8000/docs`](http://localhost:8000/docs)

### GET for all operations

`POST`, `PUT`, `PATCH`, `DELETE`? Who needs them? Just use `GET` for everything! This API does exactly that. If you want to create a new user, you `GET` a new user using the `new_user` endpoint. If you want to add a ticket, you `GET` a new ticket using the `add_ticket` endpoint. And so on.

One endpoint for each distinct action you might want to perform, and you always make a GET request, so there are no confusions.

### Terrible naming

The 4 hardest things in software development are naming things, cache invalidation, and off-by-one errors. So why stress over naming them, let's just use the first name that comes to mind when writing each endpoint.

- `GET` a new user - use the `/new_user` endpoint.
- `GET` a new ticket - use the `/add_ticket` endpoint. No need to be consistent and call it `/new_ticket` or `/ticket` or anything like that.
- `GET` an existing ticket - use the `/tikcet` endpoint. Yeah, we spelled it wrong, but we can't change it now as other teams may be using this API already and don't have time to update their code.

### Not using path parameters

We also don't want to have to worry about path parameters, as these may mean parsing the URL for the endpoint, and that sounds like hard work. You want to get a ticket? Pass the ticket ID in the bpdy of the request when calling the `/tikcet` endpoint.

Same with query parameters - we don't want to have to parse these, so we just use the body for everything. You want to seach for a ticket, call the `/search_tickets` endpoint and pass what you want to search for in the body.

`/ticket/{id}`? No thanks!

Obviously we do use path parameters for users, as one team asked for this and their boss is higher up the chain than ours. So we have `/user/{user_id}` for getting a user.

### Always returning 200

If we were to return anything except 200 from our API, then the client would throw exceptions, and this might break our users apps. This is a terrible thing, and the teams that create apps using our API might complain and blame us.

So, we always return 200. Even if the request was invalid, or the server errored, or the user doesn't have permission to perform the action. We always return 200. We can then return the actual error and status code in the body of the response. That way there are no exceptions, but the client gets the error!

### Non-atomic updates

There are engineers who think that API calls should be atomic, and if they fail then the system state should not change. We don't have time for such nonesense. We just update the database as we go, and if the request fails, then the system state is left in an inconsistent state.

For example, we have 2 tables for user data - `user` and `user_details`. When a user is created, we first create the user in the `user` table, and then create the user details in the `user_details` table. If the second request fails, then the user is left in the `user` table, but not in the `user_details` table. Yeah, so you can't recreate the user as the user email is unique, but that's the clients problem for passing us the wrong data. We can blame it on their team.

### Inconsistent data types

Each team that wants to use this API has different requirements, so we just return data in the format they expect. 

One team needs ticket IDs to feed into a CSV file, so we return these from the `/tickets` endpoint as a comma separated list of numbers. Another team wants JSON (whoever he is) for the ticket body, so we return that from the `/tikcet` endpoint. There's even a reporting team that wants XML for a list of users, so the `/user/{user_id}` endpoint returns XML.

We were also asked to handle the users salary field in different currencies, so we store that as a string. That way whatever currency they want can be added to the string.

## More terrible API practices

This repo shows a few bad practices that have actually been seen in the wild. Yea, really! But there ar emany more.

If you think of others, feel free to add a note to this repo, and even better, add them to the API itself. We can always make it worse!

You can find a fun reddit thread with more terrible examples in this [What are some of the worst API's you've ever had the displeasure of working with? What made them so bad? thread](https://www.reddit.com/r/ExperiencedDevs/comments/1ak1hof/what_are_some_of_the_worst_apis_youve_ever_had/).
