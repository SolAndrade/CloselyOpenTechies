import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CategoriesComponent } from './categories/categories.component';
import { CouponsComponent } from './coupons/coupons.component';
import { SavedComponent } from './saved/saved.component';
import { SearchComponent } from './search/search.component';


const routes: Routes = [
  { path: '', component: CategoriesComponent },
  { path: 'categories', component: CategoriesComponent },
  { path: 'saved', component: SavedComponent },
  { path: 'coupons', component: CouponsComponent },
  { path: 'search', component: SearchComponent },
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
