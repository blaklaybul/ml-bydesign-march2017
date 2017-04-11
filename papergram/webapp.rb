require 'sinatra'

get '/' do
  @image = params[:image]
  erb :index
end
