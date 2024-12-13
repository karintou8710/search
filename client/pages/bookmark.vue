<template>
    <v-container>
        <client-only>
            <!-- 表示・検索機能 -->
            <v-row>
                <v-spacer />

                <v-col
                    class="d-none d-sm-flex mx-5 mx-sm-0"
                    cols="6"
                    sm="2"
                >
                    <v-select
                        v-model="chartGridCol"
                        prepend-icon="mdi-grid-large"
                        label="grid"
                        :items="gridItems"
                    />
                </v-col>

                <v-col
                    class="mx-5 mx-sm-0"
                    cols="6"
                    sm="2"
                >
                    <v-select
                        v-model="query.ordering"
                        prepend-icon="mdi-sort-descending"
                        :items="sortItems"
                        label="Sort"
                        @change="sort"
                    />
                </v-col>
            </v-row>
        </client-only>

        <v-row>
            <v-col>
                <v-alert
                    color="blue"
                    type="info"
                >
                    あなたのブックマーク一覧
                </v-alert>
            </v-col>
        </v-row>

        <!-- main cards -->
        <v-row>
            <template v-if="!isVisible">
                <v-col
                    v-for="i in 10"
                    :key="i"
                    :cols="chartGridCol"
                >
                    <SkeletonCard />
                </v-col>
            </template>
            <template v-else>
                <v-col
                    v-for="(item, index) in items"
                    :key="item.id"
                    :cols="chartGridCol"
                >
                    <Card
                        :item="item"
                        :index="index"
                        @starClick="postBookMark(index)"
                    />
                </v-col>
            </template>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';
import MobileDetect from 'mobile-detect';
import chartMixin from '@/mixins/chart-mixin';

const protocol = process.env.PROTOCOL;
const origin = process.env.ORIGIN;
const bookmarkURL = `${protocol}://${origin}/api/bookmark/`;

export default {
    mixins: [chartMixin],
    beforeRouteUpdate (to, from, next) {
        // クエリなしに対応
        this.query.ordering = to.query.ordering || '';
        window.scrollTo(0, 0);
        this.fetchBookmarkAPIData();
        next();
    },
    head () {
        return {
            title: 'ブックマーク一覧'
        };
    },
    created () {
        if (process.server) {
            const headers = this.$nuxt.context.req.headers;
            const md = new MobileDetect(headers['user-agent']);
            this.chartGridCol = md.mobile() ? 12 : 6;
        }
    },
    async mounted () {
        this.query.ordering = this.$route.query.ordering || '';
        await this.fetchBookmarkAPIData();
        this.chartGridCol = window.innerWidth <= 600 ? 12 : 6;
    },
    methods: {

        async fetchBookmarkAPIData () {
            this.isVisible = false;

            let res;
            try {
                res = await axios.get(this.joinQuery(bookmarkURL), {
                    withCredentials: true
                });
            } catch (error) {
                if (error.response) {
                    this.$nuxt.error({
                        status: error.response.status,
                        message: 'サーバーでエラーが発生しました'
                    });
                } else if (error.request) {
                    this.$nuxt.error({
                        message: 'サーバーからレスポンスがありません'
                    });
                } else {
                    this.$nuxt.error({
                        message: error.message
                    });
                }
                return;
            }

            this.items.splice(0, this.items.length);
            this.items.push(...res.data);

            // 取得したデータがブックマーク
            this.bookMarkIDs = res.data.map(item => item.id);
            this.items.forEach((item) => {
                item.isBookMark = this.bookMarkIDs.includes(item.id);
            });

            this.isVisible = true;
        }
    }
};
</script>
