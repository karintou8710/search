<template>
    <v-container>
        <v-row>
            <v-col>
                <template v-if="error.statusCode === 404">
                    <h1>Page not found</h1>
                </template>
                <template v-else>
                    <h1>An error occurred</h1>
                    <p>status code: {{ error.statusCode }}</p>
                    <p>{{ error.message }}</p>
                </template>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    props: {
        error: {
            type: Object,
            required: true
        }
    }
};
</script>
